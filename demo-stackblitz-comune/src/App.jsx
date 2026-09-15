import { useState } from "react";
import {
  Alert,
  Breadcrumb,
  BreadcrumbItem,
  Button,
  Card,
  CardBody,
  CardText,
  CardTitle,
  Col,
  Container,
  Form,
  Header,
  HeaderBrand,
  HeaderContent,
  Headers,
  Input,
  Row,
  Select,
  TextArea,
} from "design-react-kit";

const documentInfo = {
  residenza: {
    label: "Certificato di residenza",
    description: "Attesta l'indirizzo di residenza registrato nell'anagrafe comunale.",
    delivery: "Immediata via email",
    cost: "Gratuito per uso amministrativo",
  },
  famiglia: {
    label: "Stato di famiglia",
    description: "Indica i componenti della famiglia anagrafica alla data di emissione.",
    delivery: "Immediata via email",
    cost: "Gratuito per uso amministrativo",
  },
  storico: {
    label: "Certificato storico di residenza",
    description: "Riporta i precedenti indirizzi registrati nel Comune.",
    delivery: "Entro 5 giorni lavorativi",
    cost: "Diritti di segreteria eventualmente dovuti",
  },
};

export default function App() {
  const [documentType, setDocumentType] = useState("residenza");
  const [form, setForm] = useState({ name: "", fiscalCode: "", email: "", reason: "" });
  const [receipt, setReceipt] = useState(null);
  const selectedInfo = documentInfo[documentType];

  function updateField(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  function submitRequest(event) {
    event.preventDefault();
    setReceipt({
      protocol: `DEMO-${new Date().getFullYear()}-${String(Date.now()).slice(-5)}`,
      document: selectedInfo.label,
      email: form.email,
    });
    document.querySelector("#esito")?.scrollIntoView({ behavior: "smooth" });
  }

  const isComplete = form.name && form.fiscalCode && form.email && form.reason;

  return (
    <>
      <Headers shadow>
        <Header type="slim">
          <HeaderContent>
            <span>Regione Esempio</span>
            <a className="text-white ms-auto" href="#contenuto">Vai al contenuto</a>
          </HeaderContent>
        </Header>
        <Header type="center" theme="dark">
          <HeaderContent>
            <HeaderBrand href="#" iconName="it-pa" iconAlt="Stemma segnaposto">
              <h1>Comune di Valleverde</h1>
              <p>Servizi digitali per cittadini e imprese</p>
            </HeaderBrand>
          </HeaderContent>
        </Header>
      </Headers>

      <main id="contenuto">
        <Container className="py-4 py-lg-5">
          <Breadcrumb aria-label="Percorso di navigazione">
            <BreadcrumbItem><a href="#">Home</a></BreadcrumbItem>
            <BreadcrumbItem><a href="#">Servizi</a></BreadcrumbItem>
            <BreadcrumbItem active>Richiesta documenti</BreadcrumbItem>
          </Breadcrumb>

          <Row className="align-items-start mt-3">
            <Col lg="8">
              <p className="text-uppercase fw-semibold text-primary small mb-2">Anagrafe e stato civile</p>
              <h2 className="display-5 fw-bold">Richiedi un certificato anagrafico</h2>
              <p className="lead">
                Consulta le informazioni essenziali e invia una richiesta dimostrativa.
                Nessun dato viene trasmesso o conservato.
              </p>

              <Alert color="warning" className="mt-4">
                <strong>Prototipo didattico:</strong> non inserire dati personali reali.
              </Alert>

              <section aria-labelledby="informazioni" className="mt-5">
                <h3 id="informazioni">Informazioni sul servizio</h3>
                <Row className="g-4 mt-1">
                  <Col md="6">
                    <Card border rounded fullHeight>
                      <CardBody>
                        <CardTitle tag="h4">A chi è rivolto</CardTitle>
                        <CardText>Cittadini residenti che necessitano di un certificato anagrafico.</CardText>
                      </CardBody>
                    </Card>
                  </Col>
                  <Col md="6">
                    <Card border rounded fullHeight>
                      <CardBody>
                        <CardTitle tag="h4">Cosa serve</CardTitle>
                        <CardText>Identità digitale e un indirizzo email. Nel prototipo sono simulati.</CardText>
                      </CardBody>
                    </Card>
                  </Col>
                </Row>
              </section>

              <section aria-labelledby="richiesta" className="mt-5">
                <h3 id="richiesta">Compila la richiesta</h3>
                <p>I campi contrassegnati con * sono obbligatori.</p>
                <Form onSubmit={submitRequest} className="mt-4">
                  <Select id="documentType" label="Documento richiesto *" value={documentType} onChange={setDocumentType}>
                    <option value="residenza">Certificato di residenza</option>
                    <option value="famiglia">Stato di famiglia</option>
                    <option value="storico">Certificato storico di residenza</option>
                  </Select>

                  <div className="service-preview mb-4" aria-live="polite">
                    <strong>{selectedInfo.label}</strong>
                    <p className="mb-1">{selectedInfo.description}</p>
                    <small>{selectedInfo.delivery} · {selectedInfo.cost}</small>
                  </div>

                  <Input id="name" name="name" label="Nome e cognome *" value={form.name} onChange={updateField} required />
                  <Input id="fiscalCode" name="fiscalCode" label="Codice fiscale dimostrativo *" value={form.fiscalCode} onChange={updateField} required infoText="Per la demo usare un valore inventato, ad esempio DEMO123." />
                  <Input id="email" name="email" type="email" label="Email *" value={form.email} onChange={updateField} required />
                  <TextArea id="reason" name="reason" label="Motivo della richiesta *" rows="4" value={form.reason} onChange={updateField} required />

                  <Button color="primary" size="lg" type="submit" disabled={!isComplete}>
                    Invia richiesta dimostrativa
                  </Button>
                </Form>
              </section>

              {receipt && (
                <section id="esito" className="mt-5" tabIndex="-1">
                  <Alert color="success">
                    <h3 className="h5">Richiesta acquisita</h3>
                    <p className="mb-1">Protocollo: <strong>{receipt.protocol}</strong></p>
                    <p className="mb-0">Una conferma simulata sarà inviata a {receipt.email}.</p>
                  </Alert>
                </section>
              )}
            </Col>

            <Col lg="4" className="mt-5 mt-lg-0">
              <aside className="side-panel" aria-labelledby="assistenza">
                <h3 id="assistenza" className="h5">Hai bisogno di aiuto?</h3>
                <p>Contatta l'Ufficio Anagrafe oppure prenota un appuntamento.</p>
                <dl>
                  <dt>Telefono</dt><dd>000 000000</dd>
                  <dt>Orari</dt><dd>Lun–Ven, 9:00–12:00</dd>
                </dl>
                <Button outline color="primary" href="mailto:demo@example.invalid">Contatta l'ufficio</Button>
              </aside>
            </Col>
          </Row>
        </Container>
      </main>

      <footer className="comune-footer py-4">
        <Container><strong>Comune di Valleverde</strong><p className="mb-0 mt-2">Esempio didattico basato sul Design React Kit.</p></Container>
      </footer>
    </>
  );
}

