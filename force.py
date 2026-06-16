#========================================
#    UTILS functions
#========================================
def force_int(message: str) -> int:
     while True:
          try:
               return int(input(message))
          except:
               print("Digite um numero inteiro valido")

def force_float(message: str) -> float:
     while True:
          try:
               return float(input(message))
          except:
               print("Digite um numero valido")

def force_str(message: str) -> str:
     while True:
          try:
               return str(input(message)).strip()
          except:
               print("Digite uma string valida")