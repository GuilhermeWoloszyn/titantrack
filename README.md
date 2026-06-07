TitanTrack AI

Este repositório contém a implementação da esteira de CI/CD, containerização e observabilidade do microsserviço BFF Service.



## REPOSITÓRIO

* Repositório: https://github.com/GuilhermeWoloszyn/titantrack



\---



## 1. Link dos ambientes



O deploy automático foi configurado utilizando o Render baseado na estratégia de Git Flow:



* Ambiente de DEV (Branch "develop"): https://titantrack-wgv3.onrender.com

&#x20;   - Nota: Swagger habilitado em "/docs".

* Ambiente de HOMOL (Branch "master"): https://titantrack-bfff-homol.onrender.com/

&#x20;   - Nota: Swagger desabilitado em homologação para conformidade de segurança (Retorna 404).



\---



## 2. Pipeline de CI/CD (GitHub Actions e SonarCloud)



O pipeline automatizado executa as seguintes etapas a cada push ou pull request nas branches principais:

1\.  Build e setup: Inicialização do ambiente isolado com Python 3.10.

2\.  Instalação de dependências: Configuração do ecossistema do BFF.

3\.  Testes automatizados: Execução do "pytest" com validação de cobertura via "pytest-cov".

4\.  Trava de segurança: O pipeline falha automaticamente caso a cobertura de código seja inferior a 50% (em 92% conforme os testes).

5\.  Análise de qualidade: Integração oficial com o SonarCloud para auditoria de bugs e vulnerabilidades.



\---



##  3. Segurança e Versionamento



* Segurança (Dependabot): Ativado e configurado pelo ".github/dependabot.yml" para varredura diária de vulnerabilidades em dependências do Python.
* Versionamento Semântico: Utilização de tags Git para controle de releases (Versão 1.0.0).



## Monitoramento Real

Caminho: titantrack/imagens_do_trabalho/dashboard\_metricas.png / titantrack/imagens_do_trabalho/dashboard\_numeros.png



\---



## 4. Observabilidade e Guia de Execução Local

O microsserviço expõe métricas nativas do ecossistema FastAPI através da rota `/metrics`.

### Componentes Utilizados

* **Prometheus:** Responsável pela coleta periódica das métricas expostas pelo serviço implantado no Render, realizando consultas a cada 5 segundos.
* **Grafana:** Responsável pela visualização dos dados coletados, permitindo o acompanhamento de métricas relacionadas a requisições HTTP, desempenho da aplicação e consumo de recursos.

### Evidências de Monitoramento

As capturas dos dashboards encontram-se disponíveis em:

* `titantrack/imagens_do_trabalho/dashboard_metricas.png`
* `titantrack/imagens_do_trabalho/dashboard_numeros.png`
* `titantrack/imagens_do_trabalho/dashboard_outrosnumeros.png`

---

## Instruções para Execução Local da Observabilidade

Para visualizar os dashboards consumindo métricas diretamente do ambiente de desenvolvimento hospedado no Render, siga os passos abaixo.

### Passo 1 – Inicialização dos Containers

Execute os comandos abaixo em um terminal:

```powershell
docker rm -f prometheus grafana

# Inicializar Prometheus
docker run -d --name prometheus -p 9090:9090 `
-v "C:\Caminho\Ate\A\Pasta\prometheus.yml:/etc/prometheus/prometheus.yml" `
prom/prometheus:latest

# Inicializar Grafana
docker run -d --name grafana -p 3000:3000 grafana/grafana:latest
```

### Passo 2 – Validação da Coleta de Métricas

1. Acesse `http://localhost:9090`
2. Navegue até **Status → Targets**
3. Verifique se o alvo `titantrack-wgv3.onrender.com` aparece com status **UP**

Esse status confirma que o Prometheus está coletando métricas corretamente do ambiente DEV.

### Passo 3 – Configuração do Grafana

1. Acesse `http://localhost:3000`
2. Utilize as credenciais padrão:

   * Usuário: `admin`
   * Senha: `admin`
3. Acesse **Connections → Data Sources**
4. Clique em **Add data source**
5. Selecione **Prometheus**
6. Configure a URL:

```text
http://host.docker.internal:9090
```

7. Clique em **Save & Test**

### Passo 4 – Visualização dos Dashboards

1. Acesse **Dashboards → New Dashboard**
2. Clique em **Add Visualization**
3. Selecione a fonte de dados Prometheus
4. Utilize consultas como:

**Quantidade de requisições HTTP**

```promql
http_requests_total
```

**Tempo acumulado de resposta**

```promql
http_request_duration_seconds_sum
```

5. Clique em **Run Queries** para visualizar os dados em tempo real.

Os gráficos permitirão acompanhar o comportamento das rotas disponibilizadas pelo BFF, incluindo os endpoints de autenticação e consulta de alunos.

## TODAS AS IMAGENS ACERCA DO TRABALHO ESTÃO ARMAZENADAS EM titantrack\imagens_do_trabalho