import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { styles } from '../styles';

const tabs = ['teil1', 'teil2', 'teil3', 'teil4'];

export default function A1Day25TagesablaufWorkbook() {
  const [activeTab, setActiveTab] = useState('teil1');
  const [prepared, setPrepared] = useState({ teil1: false, teil2: false, teil3: false, teil4: false });
  const [teacherMode, setTeacherMode] = useState(false);
  const [showTranscript, setShowTranscript] = useState(false);

  const renderPrepared = (key) => (
    <label>
      <input type="checkbox" checked={prepared[key]} onChange={() => setPrepared({ ...prepared, [key]: !prepared[key] })} /> I prepared this part.
    </label>
  );

  return (
    <div style={styles.pageWrapper}>
      <div style={styles.card}>
        <Link to="/campus/course" style={styles.backButton}>← Back to Course</Link>
        <h1 style={styles.title}>A1 · Day 25 Workbook · Tagesablauf</h1>
        <p style={styles.notice}>Submit all answers in the submission area, not on this page.</p>
      </div>

      <div style={styles.tabRow}>
        <button onClick={() => setActiveTab('teil1')}>Teil 1 · Sprechen</button>
        <button onClick={() => setActiveTab('teil2')}>Teil 2 · Schreiben</button>
        <button onClick={() => setActiveTab('teil3')}>Teil 3 · Lesen</button>
        <button onClick={() => setActiveTab('teil4')}>Teil 4 · Hören</button>
      </div>

      {activeTab === 'teil1' && (
        <section style={styles.card}>
          <img src="https://images.unsplash.com/photo-1506784365847-bbad939e9335" alt="Morning routine planning on a desk" loading="lazy" style={styles.image} />
          <h2>Teil 1 · Sprechen (Group Practice No assignment)</h2>
          <p>Erstellt eine Brain-Map zum Thema „Tagesablauf" mit den Bereichen Morgenroutine, Arbeit/Schule, Mittagspause, Nachmittag, Abendroutine und Freizeit.</p>
          <p><strong>Confidence self-practice:</strong> Practice aloud, then record yourself with Speech Practice.</p>
          <a href="https://www.falowen.app/campus/speech" target="_blank" rel="noreferrer">Open Speech Practice</a>
          <div>{renderPrepared('teil1')}</div>
        </section>
      )}

      {activeTab === 'teil2' && (
        <section style={styles.card}>
          <img src="https://images.unsplash.com/photo-1455390582262-044cdead277a" alt="Writing notes for a message exercise" loading="lazy" style={styles.image} />
          <h2>Teil 2 · Schreiben</h2>
          <p>Schreibe einem Freund aus dem Ausland: bedanke dich für die Einladung, erkläre warum du jetzt nicht kommen kannst, und schlage einen späteren Besuch vor.</p>
          <p>Before submission: Plan your greeting, reason, and future date suggestion. You can use the Ideas Generator in Writing Practice.</p>
          <a href="https://www.falowen.app/campus/writing" target="_blank" rel="noreferrer">Open Writing Practice</a>
          <div>{renderPrepared('teil2')}</div>
        </section>
      )}

      {activeTab === 'teil3' && (
        <section style={styles.card}>
          <img src="https://images.unsplash.com/photo-1524995997946-a1c2e315a42f" alt="Student reading comprehension text" loading="lazy" style={styles.image} />
          <h2>Teil 3 · Lesen</h2>
          <p><strong>Frage 1:</strong> Wann steht Anna auf?<br/>A) kurz vor 7 Uhr<br/>B) nie vor 7 Uhr<br/>C) immer nach 7 Uhr<br/>D) kurz nach 7 Uhr</p>
          <p><strong>Frage 2:</strong> Was isst Anna zum Frühstück?<br/>A) Cornflakes und Toast mit Butter<br/>B) nichts<br/>C) Brot mit Käse oder Wurst<br/>D) Müsli oder Toast mit Marmelade</p>
          <p><strong>Frage 3:</strong> Was macht sie nicht morgens, bevor sie zur Schule geht?<br/>A) zur Toilette gehen<br/>B) Hausaufgaben<br/>C) das Bett machen<br/>D) duschen</p>
          <p><strong>Frage 4:</strong> Wann kommt sie nach Hause?<br/>A) am Nachmittag<br/>B) nachdem sie die Hausaufgaben gemacht hat<br/>C) nach dem Abendessen<br/>D) kurz vor dem Abendessen</p>
          <p><strong>Frage 5:</strong> Was macht sie nach den Hausaufgaben?<br/>A) schlafen<br/>B) Freunde treffen<br/>C) Sport<br/>D) lernen</p>
          <div>{renderPrepared('teil3')}</div>
        </section>
      )}

      {activeTab === 'teil4' && (
        <section style={styles.card}>
          <img src="https://images.unsplash.com/photo-1469474968028-56623f02e42e" alt="Mountain vacation scene for listening task" loading="lazy" style={styles.image} />
          <h2>Teil 4 · Hören</h2>
          <label><input type="checkbox" checked={teacherMode} onChange={() => setTeacherMode(!teacherMode)} /> Teacher mode</label>
          <div style={{ marginTop: 8 }}>
            <iframe title="Day 25 hören preview" width="100%" height="315" src="https://drive.google.com/file/d/[GOOGLE_DRIVE_HOEREN_LINK]/preview" allow="autoplay" />
          </div>
          <button onClick={() => setShowTranscript(!showTranscript)}>{showTranscript ? 'Hide transcript' : 'Show transcript'}</button>
          {showTranscript && <p>Transcript: Teil 4 hat im Kursmaterial die Geschichte „Urlaub in den Bergen“ als Lesetext; nutze hier die Audio-/Teacher-Version falls bereitgestellt.</p>}
          <p><strong>Frage 1:</strong> Welches Reiseziel wählt Familie Meyer?<br/>A) Österreich<br/>B) Deutschland<br/>C) die Schweiz<br/>D) Italien</p>
          <p><strong>Frage 2:</strong> Womit fährt Familie Meyer in den Urlaub?<br/>A) mit dem Taxi<br/>B) mit dem Bus<br/>C) mit dem Auto<br/>D) mit dem Zug</p>
          <div>{renderPrepared('teil4')}</div>
        </section>
      )}
    </div>
  );
}
