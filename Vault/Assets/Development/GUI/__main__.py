import kivy
from kivy.app import App
from Payload import Payload
from LoginScreen import LoginScreen

def main():
    Payload().run()

if __name__ == '__main__':
    print(kivy.__version__)
    main()
