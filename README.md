Para rodar, é necessário instalar flask e flask_sqlalchemy

O servidor utilisa de uma base de dados PostgreSQL onde o usuário pode fazer cadastro.
Ao informar nome e cpf, o sistema verifica se o nome está associado ao cpf. 
Após isso, ao realizar login, o sistema verifica se a senha está associada ao cpf e login
Finalmente, o sistema envia um email ao email cadastrado contendo um código de 6 dígitos
e verifica se o código que o usuário inserir é o mesmo que o gerado. Assim, o financiamento
seria autorizado e o cliente poderia pagar a entrada.

O servidor é protegido de ataques SQL Injection por utilisar de SQLAlchemy, que protege
as buscas codificadas (desde que não se utilize SQL puro, o que não é o caso deste código)
