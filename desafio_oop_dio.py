from abc import *
import textwrap

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo
    
    @saldo.setter
    def saldo(self, valor):
        self._saldo = valor

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
            return True
        else:
            return False
        
    def depositar(self, valor):
        self.saldo += valor
        return True
    
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)
        
class Historico:
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)
        
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(self, conta):
        pass
    
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self.name = __class__.__name__
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        conta.depositar(self.valor)
        conta.historico.adicionar_transacao({'tipo': self.name, 'valor': self.valor})
        
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self.name = __class__.__name__
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        conta.sacar(self.valor)
        conta.historico.adicionar_transacao({'tipo': self.name, 'valor': self.valor})
        
class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
    
    @property
    def pf_cliente(self):
        return {
            'nome': self.nome,
            'cpf': self.cpf,
            'data_nascimento': self.data_nascimento,
            'endereco': self.endereco
        }
        
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=1000, limite_saques=5):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
    
    @property
    def limite(self):
        return self._limite
    
    def sacar(self, valor):
        if self.historico.transacoes.count(Saque) >= self._limite_saques:
            return False
        elif valor <= self.limite:
            return super().sacar(valor)
        else:
            return False
        
    @property
    def pf_conta(self):
        return {
            'agencia': self.agencia,
            'numero': self.numero,
            'cliente': self.cliente
        }
        
    def __str__(self):
        return f"""
            Agencia: {self.agencia}
            Conta Corrente: {self.numero}
            Titular: {self.cliente}
        """
        
class Menu:
    def __init__(self):
        self.opcoes = {
            0: ['Novo cliente', 'novo_cliente'],
            1: ['Nova conta', 'nova_conta'],
            2: ['Listar contas', 'listar_contas'],
            3: ['Depositar', 'depositar'],
            4: ['Sacar', 'sacar'],
            5: ['Extrato', 'extrato'],
            6: ['Sair', 'sair']
        }
        self.clientes = []
        self.contas = []
        self.run()

    def run(self):
        while True:
            for key, value in self.opcoes.items():
                print(f'{key}: {value[0]}')
            choice = int(input('Escolha uma opção: '))
            if choice in self.opcoes:
                getattr(self, self.opcoes[choice][1])()
            else:
                print('Opção inválida.')

    def filtrar_cliente(self, cpf):
        for cliente in self.clientes:
            if cliente.pf_cliente['cpf'] == cpf:
                return cliente
        return None
    
    def filtrar_conta(self, numero):
        for conta in self.contas:
            if conta.pf_conta['numero'] == numero:
                return conta
        return None

    def novo_cliente(self):
        print('Criar Novo cliente')
        cpf = input('Digite o seu CPF (somente números): ')
        isCliente = self.filtrar_cliente(cpf)
        if isCliente:
            print('Cliente já cadastrado.')
        else:
            nome = input('Digite o seu nome: ')
            data_nascimento = input('Digite a sua data de nascimento (dd/mm/aaaa): ')
            endereco = input('Digite o seu endereço: ')
            cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)
            self.clientes.append(cliente)
            print('Cliente cadastrado com sucesso.')
            
    def nova_conta(self):
        print('Nova conta')
        cpf = input('Digite o seu CPF (somente números): ')
        isCliente = self.filtrar_cliente(cpf)
        if isCliente:
            numero_conta = len(self.contas) + 1
            conta = ContaCorrente.nova_conta(numero=numero_conta, cliente=isCliente.pf_cliente)
            self.contas.append(conta)
            print(isCliente.pf_cliente)
            isCliente.contas.append(conta)
            print('Conta criada com sucesso.')
        else:
            print('Cliente não encontrado.')
        
    def listar_contas(self):
        for conta in self.contas:
            print('='*20)
            print(textwrap.dedent(str(conta)))
            print('='*20)

    def depositar(self):
        print('Depositar')
        cpf = input('Digite o seu CPF (somente números): ')
        isCliente = self.filtrar_cliente(cpf)
        if not isCliente:
            print('Cliente não encontrado.')
            return
        conta = int(input('Digite o número da conta: '))
        isConta = self.filtrar_conta(numero=conta)
        if isConta:
            valor = float(input('Digite o valor do depósito: '))
            transacao = Deposito(valor)
            isCliente.realizar_transacao(isConta, transacao)
            print('='*20)
            print(f'Depósito de R${valor} realizado com sucesso.')
            print('='*20)
        else:
            print('Conta não encontrada.')
            return

    def sacar(self):
        print('Sacar')
        cpf = input('Digite o seu CPF (somente números): ')
        isCliente = self.filtrar_cliente(cpf)
        if not isCliente:
            print('Cliente não encontrado.')
            return
        conta = int(input('Digite o número da conta: '))
        isConta = self.filtrar_conta(numero=conta)
        if isConta:
            valor = float(input('Digite o valor do saque: '))
            transacao = Saque(valor)
            isCliente.realizar_transacao(isConta, transacao)
            print('='*20)
            print(f'Saque de R${valor} realizado com sucesso.')
            print('='*20)
        else:
            print('Conta não encontrada.')
            return

    def extrato(self):
        print('Extrato')
        cpf = input('Digite o seu CPF (somente números): ')
        isCliente = self.filtrar_cliente(cpf)
        if not isCliente:
            print('Cliente não encontrado.')
            return
        conta = int(input('Digite o número da conta: '))
        isConta = self.filtrar_conta(numero=conta)
        if isConta:
            transacoes = isConta.historico.transacoes
            if not transacoes:
                print('Sem transações.')
            else:
                for transacao in transacoes:
                    print(transacao)

    def sair(self):
        print('Sair')
        exit(0)

if __name__ == "__main__":
    Menu()