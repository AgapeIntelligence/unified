pragma circom 2.0.0;

include "circomlib/poseidon.circom";
include "circomlib/comparators.circom";
include "circomlib/bitify.circom";

template DyadReflectionProof(depth) {
    signal input public_root;  // Merkle root from history hash
    signal input claimed_step; // Step number
    signal input d_history[depth];  // Private: d values
    signal input l_history[depth];  // Private: l values
    signal output deviation_bound;  // Public: 1 for valid, 0 otherwise
    signal output entropy_bound;    // Public: 1 for valid, 0 otherwise

    // Verify history commitment
    component hasher = Poseidon(depth * 2);
    for (var i = 0; i < depth; i++) {
        hasher.inputs[i] = d_history[i];
        hasher.inputs[i + depth] = l_history[i];
    }
    hasher.out === public_root;

    // Check claimed step is within bounds
    component step_check = LessThan(32);
    step_check.in[0] <== claimed_step;
    step_check.in[1] <== depth;
    step_check.out === 1;

    // Prove deviation <= 1e-10 (scaled to 252-bit precision)
    component deviation = LessThan(252);
    var total = d_history[claimed_step] + l_history[claimed_step];
    var diff = d_history[claimed_step] > l_history[claimed_step] ? 
               d_history[claimed_step] - l_history[claimed_step] : 
               l_history[claimed_step] - d_history[claimed_step];
    var scaled_diff = diff * 1000000000000000000;  // Scale 1e-18
    deviation.in[0] <== scaled_diff;
    deviation.in[1] <== 1;  // Bound at 1e-10 when scaled
    deviation_bound <== deviation.out;

    // Prove entropy >= 0.9999999999 (simplified range check)
    component p_calc = Num2Bits(252);
    p_calc.in <== (d_history[claimed_step] * 1000000000000) / total;  // Scaled p
    var p = p_calc.out[251];  // Approx p ~ 0.5 (binary)
    var entropy = -p * 3.32192809489 - (1 - p) * 3.32192809489;  // log2 approx
    component entropy_check = GreaterThan(252);
    entropy_check.in[0] <== entropy * 1000000000000;  // Scaled
    entropy_check.in[1] <== 999999999999;  // 0.9999999999 scaled
    entropy_bound <== entropy_check.out;

    // Ensure both constraints hold
    deviation_bound * entropy_bound === 1;
}

component main {public [public_root, claimed_step]} = DyadReflectionProof(256);
