# Sistema de Gestão das Olimpíadas (SGO)

> **PUC Minas — Engenharia de Software — Projeto de Software**  
> Professor: João Paulo Carneiro Aramuni  
> Trabalho 1 SGO  
> Grupo: Mateus Ferrão e Felipe Fontenelle

## Descrição

Sistema para coordenar os aspectos das Olimpíadas: gerenciamento de competições, inscrições de atletas, alocação de locais e controle de resultados com quadro de medalhas por país.

**Stack conceitual:** Node.js · TypeScript · React · PostgreSQL · Docker

---

## Regras de Negócio

1. **Cadastro de competições** — modalidade, data, horário, local e lista de atletas inscritos.
2. **Inscrição de atletas** — cada atleta pode participar de várias competições, mas só representa **um país por modalidade**.
3. **Alocação de locais** — um local abriga **apenas uma competição por vez** (sem conflito de horário).
4. **Controle de resultados** — 1º (ouro), 2º (prata) e 3º (bronze) por competição.
5. **Relatório de medalhas** — desempenho de cada país agrupado por tipo de medalha.

---

## Decisões de Modelagem

- **Casos de uso:** as regras críticas foram representadas como validações incluídas, como validar disponibilidade do local, validar país por modalidade e verificar inscrições antes do registro de resultado.
- **Classes:** a classe `Inscricao` liga atleta, competição e país representado, permitindo controlar a regra de que o atleta representa apenas um país por modalidade.
- **Pacotes:** a solução separa apresentação, controllers, casos de uso, domínio, interfaces de repositório e infraestrutura.
- **Componentes:** foram criadas duas versões. A versão principal usa interfaces fornecidas e requeridas; a versão secundária mantém dependências diretas para facilitar a leitura quando a renderização do PlantUML fica visualmente poluída.
- **Implantação:** a arquitetura física considera navegador, Nginx, API Node.js, PostgreSQL e volume Docker para persistência.

---

## Histórias de Usuário

| ID | Ator | Como... | Quero... | Para... |
|----|------|---------|----------|---------|
| US01 | Administrador | administrador do sistema | cadastrar competições com modalidade, data, horário e local | organizar o calendário olímpico |
| US02 | Administrador | administrador do sistema | alocar um local a uma competição verificando disponibilidade de horário | evitar conflitos de agenda entre competições |
| US03 | Administrador | administrador do sistema | registrar o resultado de uma competição com 1º, 2º e 3º colocados | documentar os vencedores oficialmente |
| US04 | Administrador | administrador do sistema | gerar o relatório de medalhas agrupado por país (ouro, prata e bronze) | divulgar o quadro olímpico atualizado |
| US05 | Administrador | administrador do sistema | cadastrar atletas com seus dados pessoais e país de origem | manter o cadastro de participantes |
| US06 | Administrador | administrador do sistema | cadastrar locais de competição com nome, capacidade e endereço | disponibilizar venues para alocação |
| US07 | Atleta | atleta cadastrado no sistema | inscrever-me em uma competição escolhendo o país que vou representar naquela modalidade | participar oficialmente da modalidade olímpica |
| US08 | Atleta | atleta cadastrado no sistema | visualizar todas as competições com datas, horários e locais | planejar minha participação nas provas |
| US09 | Atleta | atleta cadastrado no sistema | consultar meus resultados nas competições em que participei | acompanhar meu desempenho olímpico |
| US10 | Visitante | visitante ou público geral | consultar o quadro de medalhas atualizado por país | acompanhar o desempenho das nações nas Olimpíadas |

---

## Diagramas UML

### Diagrama de Caso de Uso

Contempla os atores Administrador, Atleta e Visitante, além dos fluxos principais e validações obrigatórias.

<img width="700px" src="imagens/diagrama-de-caso-de-uso.png"/>

### Diagrama de Classes

Representa competições, atletas, locais, inscrições, países, resultados e relatório de medalhas, com restrições de negócio indicadas em notas.

<img width="700px" src="imagens/diagrama-de-classes.png"/>

### Diagrama de Pacotes

Organiza o sistema em frontend, backend, domínio, casos de uso, infraestrutura e banco de dados.

<img width="700px" src="imagens/diagrama-de-pacotes.png"/>

### Diagrama de Componentes - Opção Principal

Mostra componentes consumidores e fornecedores por meio de interfaces requeridas e fornecidas.

<img width="700px" src="imagens/diagrama-de-componentes.png"/>

### Diagrama de Componentes - Segunda Opção Sem Requisições

Versão simplificada sem interfaces requeridas e fornecidas, mantendo dependências diretas entre os componentes para facilitar a leitura.

> Observação: ao representar todas as interfaces requeridas e fornecidas no PlantUML, a renderização pode ficar muito poluída e desorganizada. Por isso, esta segunda opção também foi incluída como alternativa visual mais limpa.

<img width="700px" src="imagens/diagrama-de-componentes-sem-requisições.png"/>

### Diagrama de Implantação

Distribui a aplicação em navegador, containers Docker, API, proxy reverso, banco de dados e volume persistente.

<img width="700px" src="imagens/diagrama-de-implantacao.png"/>

---

## Arquitetura do Sistema

### Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| Frontend | React 18 + TypeScript + Vite |
| Backend | Node.js 20 + TypeScript + Express |
| ORM | TypeORM |
| Banco de Dados | PostgreSQL 15 |
| Infraestrutura | Docker + Docker Compose |
| Proxy Reverso | Nginx (alpine) |

### Estrutura de Diretórios (conceitual)

```
sgo/
├── frontend/               # React + TypeScript (Vite)
│   ├── src/
│   │   ├── pages/          # CompeticoesPage, AtletasPage, ResultadosPage, RelatoriosPage
│   │   ├── components/     # CompetitionCard, AthleteForm, MedalTable, ResultForm
│   │   └── services/       # ApiService, CompetitionService, AthleteService
│   └── Dockerfile
├── backend/                # Node.js + Express + TypeScript
│   ├── src/
│   │   ├── controllers/    # CompetitionController, AthleteController, ResultController...
│   │   ├── use-cases/      # CadastrarCompeticao, InscreverAtleta, AlocarLocal...
│   │   ├── domain/
│   │   │   ├── entities/   # Competicao, Atleta, Local, Resultado, Pais, Inscricao
│   │   │   └── repositories/ # interfaces ICompetitionRepo, IAthleteRepo...
│   │   └── infrastructure/ # implementações TypeORM, migrations
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Estrutura do Repositório

```
sistema-gestao-olimpiadas/
├── README.md
├── gerar_imagens.py             # script para regenerar PNGs via PlantUML API
├── imagens/
│   ├── diagrama-de-caso-de-uso.png
│   ├── diagrama-de-classes.png
│   ├── diagrama-de-pacotes.png
│   ├── diagrama-de-componentes.png
│   ├── diagrama-de-componentes-sem-requisições.png
│   └── diagrama-de-implantacao.png
└── codigos/
    ├── diagrama-de-caso-de-uso.puml
    ├── diagrama-de-classes.puml
    ├── diagrama-de-pacotes.puml
    ├── diagrama-de-componentes.puml
    ├── diagrama-de-componentes-sem-requisições.puml
    └── diagrama-de-implantacao.puml
```
