import React from 'react';
import { Link } from 'react-router-dom';
import { styles } from '../styles';

const A1Day25TagesablaufWorkbook = () => {
  return (
    <div style={styles.pageWrapper}>
      <div style={styles.card}>
        <Link to="/campus/course" style={styles.backButton}>← Back to Course</Link>
        <h1 style={styles.title}>A1 · Day 25 Workbook · Tagesablauf</h1>
        <p style={styles.subtitle}>Chapter 9.25</p>
        <p style={styles.notice}>
          Bitte reiche deine Antworten im Submission-Bereich ein, nicht direkt auf dieser Seite.
        </p>
      </div>

      <section style={styles.card}>
        <h2>Teil 1 (Sprechen) · Group Practice</h2>
        <h3>Tagesablauf (Exercise) 9.25</h3>
        <p>Erstellt eine Brain-Map mit dem zentralen Thema <strong>„Tagesablauf“</strong>.</p>
        <img
          src="[UNSPLASH_URL]"
          alt="Illustration einer täglichen Routine für die Sprechübung"
          loading="lazy"
          style={styles.image}
        />
        <h4>Hauptzweige</h4>
        <ul>
          <li>Morgenroutine</li>
          <li>Arbeit/Schule</li>
          <li>Mittagspause</li>
          <li>Nachmittag</li>
          <li>Abendroutine</li>
          <li>Freizeit und Hobbys</li>
        </ul>
        <p><strong>Leitfrage:</strong> Wie sieht dein Tagesablauf aus? (aufstehen, arbeiten/lernen, essen, Freizeit)</p>
      </section>

      <section style={styles.card}>
        <h2>Teil 2 (Schreiben)</h2>
        <p>
          Ein Freund aus dem Ausland hat dich eingeladen. Du kannst im Moment nicht kommen.
          Schreibe eine Nachricht.
        </p>
        <ul>
          <li>Bedanke dich für die Einladung.</li>
          <li>Erkläre, warum du zurzeit nicht kommen kannst.</li>
          <li>Schlage einen späteren Besuch vor.</li>
        </ul>
      </section>

      <section style={styles.card}>
        <h2>Teil 3 (Lesen) · Mein Tag</h2>
        <ol>
          <li>Wann steht Anna auf? <strong>a) kurz vor 7 Uhr</strong></li>
          <li>Was isst Anna zum Frühstück? <strong>d) Müsli oder Toast mit Marmelade</strong></li>
          <li>Was macht sie nicht morgens? <strong>b) Hausaufgaben</strong></li>
          <li>Wann kommt sie nach Hause? <strong>a) am Nachmittag</strong></li>
          <li>Was macht sie nach den Hausaufgaben? <strong>b) Freunde treffen</strong></li>
        </ol>
      </section>

      <section style={styles.card}>
        <h2>Teil 4 (Lesen) · Urlaub in den Bergen</h2>
        <p><em>Hinweis: Teil 4 ist ebenfalls Lesen (kein Hören).</em></p>
        <ol>
          <li>Welches Reiseziel wählen die Meyers? <strong>c) die Schweiz</strong></li>
          <li>Womit fahren sie in den Urlaub? <strong>d) mit dem Zug</strong></li>
          <li>Wo steigen sie aus dem Zug? <strong>a) an einem kleinen Bahnhof</strong></li>
          <li>Was erhalten sie an der Rezeption? <strong>d) einen Zimmerschlüssel</strong></li>
          <li>Warum ist Herr Meyer unzufrieden? <strong>b) das Zimmer ist zu klein</strong></li>
        </ol>
        <p>
          Hören-Link (falls vom Kurs genutzt):{' '}
          <a href="[GOOGLE_DRIVE_HOEREN_LINK]" target="_blank" rel="noreferrer">Google Drive</a>
        </p>
      </section>

      <section style={styles.calloutCard}>
        <h3>Final Submission</h3>
        <p>Bitte sende alle Antworten im Submission-Bereich.</p>
        <a href="https://www.falowen.app/campus/submit" target="_blank" rel="noreferrer" style={styles.ctaButton}>
          Zur Submission Area
        </a>
      </section>
    </div>
  );
};

export default A1Day25TagesablaufWorkbook;
