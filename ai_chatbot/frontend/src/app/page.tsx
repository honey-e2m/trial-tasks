import Head from 'next/head';

export default function Home() {
  return (
    <main style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '2rem'
    }}>
      <h1 style={{ fontSize: '3rem', fontWeight: '800', letterSpacing: '-0.05em' }}>
        E2M Solutions
      </h1>
      <p style={{ maxWidth: '600px', textAlign: 'center', color: 'hsl(var(--muted-foreground))' }}>
        This is a demo page representing the E2M Solutions website.
        The chatbot widget should appear in the bottom right corner.
      </p>
      {/* The ChatWidget will be added in layout.tsx or here */}
    </main>
  );
}
