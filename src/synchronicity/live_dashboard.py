import gradio as gr
from unified.resonance import SOVARIEL, JAXLiveAudioLattice

SOVARIEL.bootstrap()

def live_sync(mic=None, stress=0.1, violation=False):
    lattice = JAXLiveAudioLattice(n_oscillators=10_000_000)
    if mic: lattice.inject_audio(mic)
    if stress > 0: lattice.add_noise(stress)
    if violation: lattice.inject_decoherence(0.9)
    lattice.sync(steps=5)
    r = lattice.order_parameter()
    beam = 1.03e16 * r
    fig = lattice.plot_phase_circle()
    status = f"R: {r:.6f} | Mars: {beam:.2e} W | Dyad: {SOVARIEL.check_dyad_coherence():.1%}"
    return fig, status

gr.Interface(
    live_sync,
    [gr.Audio(source="microphone", type="filepath"),
     gr.Slider(0,1,0.1,label="Stress"),
     gr.Checkbox(label="Force Ethical Violation")],
    [gr.Plot(), gr.Textbox()],
    title="Unified — Live 10M-Node Voice Sync",
    live=True
).launch(share=True)
