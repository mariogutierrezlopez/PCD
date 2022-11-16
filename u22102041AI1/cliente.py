import threading #Librería para instanciar hilos
import sys #Funciones del sistema
import socket #Para hablar con otra consola
import pickle #Pasar a binario de forma mas rapida
import os #Sistema operativo

class Cliente(): #Clase cliente
	#Funcion init: Arranca el sistema con la IP y el puerto
	def __init__(self, host=input("Intoduzca la IP del servidor ?  "), port=int(input("Intoduzca el PUERTO del servidor ?  "))):
		#Pregunta al sistema la IP y el puerto
		self.s = socket.socket()
		nickname = input("Introduce el nickname: ")
		while (nickname == ""):
			nickname = input("Introduce el nickname correctamente: ")
		self.nickname = nickname
		self.s.connect((host, int(port))) #Me conecto al host y el puerto ("Es como un numero de telefono")
		#Imprime el estado del programa
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		
		#instanciamos un hilo demonio para que reciba la llamada, llama a recibir

		threading.Thread(target=self.recibir, daemon=True).start()

		#Envío el nombre de usuario al servidor 
		self.s.send(pickle.dumps(self.nickname))
		
		#Un while que está todo el tiempo escuchando
		while True:
			msg = input('\nEscriba texto ?   ** Enviar = ENTER   ** Salir Chat = 1 \n') #Recibe el texto
			if msg != '1' : self.enviar(msg) #Si el mensaje no es 1 envia el mensaje
			else: #Si el mensaje es 1 se cierra el socket
				print(" **** Me piro vampiro; cierro socket y mato al CLIENTE con PID = ", os.getpid())
				self.s.close()
				sys.exit()
				#Si dejo abierto el socket, eso se queda ahí, "como cuando reservas una habitación de hotel y no la cancelas"

	#Función recibir
	def recibir(self):
		#Te imprime quien es el que está manejando recibir
		print('\nHilo RECIBIR con ID =',threading.currentThread().getName(), '\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		#Bucle while que va a estar siempre escuchando
		while True:
			try:
				data = self.s.recv(32) #Creo una variable data que recibe el dato de alguien que ha escrito en el chat
					#El método es el método receive dentro del socket
					#32 --> Es la longitud del mensaje, cuanto más rapido mejor
				if data: print(pickle.loads(data)) #Imprimo lo que viene del otro lado de recibir
					#El método pickle es para convertir de binario a lenguaje natural
			except: pass #Si ocurre un error, que siga dando vueltas

	#Función enviar
	def enviar(self, msg):
		self.s.send(pickle.dumps(self.nickname + ": " + msg))
		with open("u22102041AL1.txt", "a") as f:
			f.write(self.nickname + ": " + msg + "\n")
		#Método send que tiene socket
		#El método pickle.dumps() convierte de lenguaje natural a binario

arrancar = Cliente()

		