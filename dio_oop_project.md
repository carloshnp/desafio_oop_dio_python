The following project is:

# OOP Banking System

class Conta:

    1. Private variables
        - saldo: float
        - numero: int
        - agencia: str
        - cliente: composition class
        - historico: composition class
    2. Public methods:
        + saldo(): float
        + nova_conta(cliente: Cliente, numero: int): Conta
        + sacar(valor: float): bool
        + depositar(valor: float): bool

class Cliente: composition class from conta; cardinality zero or more to Conta, cardinality 1 to Cliente, cardinality zero or more to Transacao

    1. Private variables:
        - endereco: str
        - contas: list
    2. Public methods:
        + realizar_transacao(conta: Conta, transacao: Transacao)
        + adicionar_conta(conta: Conta)

class Historico: composition class from conta; cardinality 1 to historico

    1. Public methods:
        + adicionar_transacao(transacao: Transacao)

interface Transacao: aggregation class to Historico; cardinality zero or more from Historico

    1. Public methods:
        + registrar(conta: Conta)

class Deposito: inherits from Transacao

    1. Private variables:
        - valor: float

class Saque: inherits from Transacao

    1. Private variables:
        - valor: float

class PessoaFisica: inherits from Cliente

    1. Private variables:
        - cpf: str
        - nome: str
        - data_nascimento: date

class ContaCorrente: inherits from Conta

    1. Private variables:
        - limite: float
        - limite_saques: int