import flet as ft
from flet_core.control_event import ControlEvent
from flet import FilePicker, Row, Text
from transformers import pipeline
import sounddevice
from scipy.io.wavfile import write, read

def main(page: ft.Page):
    page.title = "Wani"
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN



    def updateTrans(x: str):
        t.value = x
        t.update()

    def updateName(x:str):
        fileName.value = x;
        fileName.update()
        
        fileDisp.bgcolor = "#D3D3D3"
        fileDisp.content = ft.Row([fileName,playButton],alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        fileDisp.update()

    def transcribe(path: str,e: ControlEvent):

        whisper = pipeline('automatic-speech-recognition',model="models--openai--whisper-medium")
        text = whisper(path)
        print(text)
        updateTrans(text["text"])

    def record(e: ControlEvent):
        updateTrans("Recording...")
        fps = 44100
        duration = 20
        print("Recording...")
        global recording
        recording = sounddevice.rec(int(duration*fps),samplerate=fps,channels=2)
        sounddevice.wait()
        print("Done")
        updateTrans("Transcribing...")

        write("output.wav",fps,recording)

        transcribe("output.wav",ControlEvent)


    def stopRecording(e):
        updateTrans("Transcribing...")
        sounddevice.stop()

        write("output.wav",44100,recording)
        transcribe("output.wav",ControlEvent)


    def onRes(e: ft.FilePickerResultEvent):
        print("Selected: ",e.files)
        print("Path: ",e.files[0].path)
        global audioFilePath
        audioFilePath = str(e.files[0].path)
        updateName(str(e.files[0].name))
        updateTrans("Transcribing...")
        transcribe(audioFilePath,ControlEvent)

    def playRecording(e):
        print("Playing the audio File")
        (fs1, x) = read(audioFilePath)
        sounddevice.play(x, fs1)
        sounddevice.wait
    
    filePicker: FilePicker = FilePicker(on_result=onRes)
    page.overlay.append(filePicker)
    page.update()

    t = ft.Text("Choose file or Record audio to generate Transcription")
    fileName = ft.Text("")
    fileDisp = ft.Container(bgcolor="#FFFFFF",content=ft.Row([fileName]),padding=10,border_radius=10)

    buttonTrans: ft.ElevatedButton = ft.ElevatedButton("Choose Files",on_click=lambda _ : filePicker.pick_files(allow_multiple=False))
    buttonrec: ft.ElevatedButton = ft.ElevatedButton("Record",on_click=lambda _ : record(ControlEvent))
    buttonStopRec: ft.IconButton = ft.IconButton(ft.icons.STOP,on_click=lambda _ : stopRecording(ControlEvent))
    playButton: ft.IconButton = ft.IconButton(ft.icons.PLAY_ARROW,on_click=lambda _ : playRecording(ControlEvent))


    logo = ft.Image(
        src="assets/drdo_logo.png"
    )

    page.appbar = ft.AppBar(
        leading= logo,
        title=Text("Wani",size=30,weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor="#73C2FB"
    )
    page.update()

    page.add(
        t,
        ft.ResponsiveRow(
            [
                buttonTrans,
                buttonrec,
                buttonStopRec,
                fileDisp,
            ]
        ),
    )

if __name__ == "__main__":
    ft.app(target=main)