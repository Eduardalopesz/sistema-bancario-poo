class PessoaFisica:
    def _init_(self, cpf, nome, data_nascimento):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Cliente:
    def _init_(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Historico:
    def _init_(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Conta:
    def _init_(self, saldo, numero, agencia, cliente):
        self.saldo = saldo
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo(self):
        return self.saldo

    def nova_conta(cls, cliente, numero):
        return cls(0, numero, "0001", cliente)

    def sacar(self, valor):
        if valor > self.saldo:
            return False
        self.saldo -= valor
        return True

    def depositar(self, valor):
        if valor <= 0:
            return False
        self.saldo += valor
        return True

class ContaCorrente(Conta):
    def _init_(self, saldo, numero, agencia, cliente, limite, limite_saques):
        super()._init_(saldo, numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

class Transacao:
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def _init_(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(f"Depósito: R$ {self.valor:.2f}")

class Saque(Transacao):
    def _init_(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(f"Saque: R$ {self.valor:.2f}")

clientes = []
contas = []
numero_conta = 1
limite = 500
LIMITE_SAQUES = 3

def cadastrar_cliente(cpf, nome, data_nascimento, endereco):
    cliente = Cliente(endereco)
    cliente_pessoa = PessoaFisica(cpf, nome, data_nascimento)
    clientes.append(cliente)
    return cliente

def criar_conta_corrente(cliente):
    global numero_conta
    conta = ContaCorrente(0, numero_conta, "0001", cliente, limite, LIMITE_SAQUES)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    numero_conta += 1
    return conta

def depositar(conta, valor):
    deposito = Deposito(valor)
    deposito.registrar(conta)

def sacar(conta, valor):
    saque = Saque(valor)
    saque.registrar(conta)

def extrato(conta):
    print("\n================ EXTRATO ================")
    for transacao in conta.historico.transacoes:
        print(transacao)
    print(f"Saldo: R$ {conta.saldo:.2f}")
    print("==========================================")
