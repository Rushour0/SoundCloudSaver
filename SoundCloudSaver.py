from sclib import SoundcloudAPI, Track, Playlist
import PySimpleGUI as sg
from googlesearch import search

sg.LOOK_AND_FEEL_TABLE['MyCreatedTheme'] = {'BACKGROUND': '#2B202B','TEXT': '#FFCC66','INPUT': '#339966','TEXT_INPUT': '#000000','SCROLL': '#99CC99','BUTTON': ('#003333', '#AABBCC'),'PROGRESS': ('#D1826B', '#CC8019'),'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0, }
sg.theme('MyCreatedTheme')

layout = [[sg.Text("Enter song name and artist")],
          [sg.Input(size = (40,1),key = 'searchstr' ),sg.Button('  search  ')],
          [sg.Text(size = (40,1),key = 'searched',background_color = "#AABB99"),sg.Button('  save file  ')],
          [sg.Text(size = (40,1),key = 'out',text_color = "#CC55AA")],
          [sg.Button('  quit  ')]]
api = SoundcloudAPI()
def download(resultstr):
    track = api.resolve(f"{resultstr}")

    if type(track) is not Track:
        return

    filename = f"./{track.title}_{track.artist}.mp3"

    with open(filename,"wb+") as fn:
        try:
            track.write_mp3_to(fn)
            window['out'].update("saved")
        except:
            print("err")
            return

def searchMe(searchstr):
    searched = [x for x in search(f"sound cloud {searchstr}",num_results = 1)]
    return searched


def loop():
    layout = [[sg.Text("Enter song name and artist")],
          [sg.Input(size = (40,1),key = 'searchstr' ),sg.Button('  search  ')],
          [sg.Text(size = (40,1),key = 'searched',background_color = "#AABB99"),sg.Button('  save file  ')],
          [sg.Text(size = (40,1),key = 'out',text_color = "#CC55AA")],
          [sg.Button('  quit  ')]]
    window = sg.Window('Sound Cloud Download', layout,margins = (100,100))
    searched = ''
    while True:
        event, values = window.read()

        if event == '  search  ':
            if values['searchstr'].strip() != '':
                searched = searchMe(values['searchstr'].strip())
                window['searched'].update(' '.join(searched),text_color = "black")
                rescount = -1
            else:
                window['out'].update("bavlat")
                window['searched'].update('')
        if event == '  save file  ':
            if len(searched)!=rescount-1:
                rescount+=1
            
            download(searched[rescount])
        if event == sg.WINDOW_CLOSED or event == '  quit  ':
            res = sg.popup_yes_no("Do you want to quit?")
            if res.lower() == "yes":
                break
            else:
                loop()
                break
    window.close()
loop()

