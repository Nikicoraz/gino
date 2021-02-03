from time import sleep
from threading import Thread

class Timer:
    def __init__(self, seconds : int):
        '''
        Classe Timer

        Arguments:

        __init_seconds : int = Secondi dati dall'utente
        _seconds_passed : int = secondi contati dal timer
        __end_func : list = Lista di funzioni da eseguire alla fine del timer
        _stop : bool = Se il timer è stato fermato con stop()
        _seconds : int = Secondi da contare
        running : bool = Se sta andando il timer
        '''
        self.__init_seconds = seconds
        self._seconds_passed = 0
        self.__end_func = []
        self._stop = False
        self._seconds = self.__init_seconds
        self.running = False

    def __end(self):
        '''
        Cose da fare quando finisce il timer
        '''
        for func in self.__end_func:
            func()

    def call_at_end(self, *args):
        '''
        Aggiungere funzioni da eseguire a fine timer
        '''
        for func in args:
            self.__end_func.append(func)

    def start(self):
        '''
        Far partire o riprendere il timer.
        Meglio farlo partire dentro un Thread per farlo contare a parte
        '''
        self._seconds_passed = self.__init_seconds - self._seconds
        self.running = True
        for i in range(self._seconds):
            if self.running:
                sleep(1)
                self._seconds_passed += 1
        if self.running: 
            self.__end()
            self.running = False
        elif self._stop:
            self._stop = False
        else:
            self.start()

    def get_seconds(self):
        '''
        Restituisci quanti secondi sono passati dall'inizio del timer
        '''
        return self._seconds_passed

    def get_remaining_seconds(self):
        '''
        Restituisce quanti secondi mancano alla fine del timer
        '''
        return self._seconds - self._seconds_passed
    
    def stop(self):
        '''
        Ferma il timer e resetta i secondi a 0
        '''
        self._stop = True
        self.running = False
        self._seconds = self.__init_seconds
    
    def reset(self):
        '''
        Resetta il timer rimettendo i secondi a 0 e facendolo ripartire
        '''
        self.running = False

    def pause(self):
        '''
        Mette in pausa il timer.
        Riprendi usando start()
        '''
        self._stop = True
        self.running = False
        seconds_remaining = self.get_remaining_seconds()
        self._seconds = seconds_remaining
        

if __name__ == '__main__':
    def hello_world(pizza):
        print('hello world!' + pizza)
    t = Timer(10)
    t.call_at_end(lambda:hello_world('ciao'))
    d = Thread(target=t.start)
    d.start()
    while True:
        sleep(1)
        print(t.get_seconds())