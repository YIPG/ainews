import React from 'react';

export interface NewsletterTemplateProps {
  title: string;
  date: string;
}

export function NewsletterTemplate({ title, date }: NewsletterTemplateProps) {
  return (
    <div
      style={{
        display: 'flex',
        height: '100%',
        width: '100%',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#0F2027',
        backgroundImage: 'linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%)',
        fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
        position: 'relative',
      }}
    >
      {/* Circuit pattern overlay */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          opacity: 0.1,
          display: 'flex',
          flexWrap: 'wrap',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {Array.from({ length: 20 }).map((_, i) => (
          <div
            key={i}
            style={{
              width: '100px',
              height: '100px',
              border: '1px solid white',
              borderRadius: '50%',
              margin: '20px',
            }}
          />
        ))}
      </div>

      {/* Main content card */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: 'rgba(255, 255, 255, 0.08)',
          borderRadius: '24px',
          padding: '80px',
          maxWidth: '900px',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          boxShadow: '0 20px 40px rgba(0, 0, 0, 0.3)',
          position: 'relative',
        }}
      >
        {/* Brand logo */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            marginBottom: '40px',
            fontSize: '32px',
            color: 'rgba(255, 255, 255, 0.9)',
          }}
        >
          <span style={{ marginRight: '12px' }}>✏️</span>
          <span style={{ fontWeight: 600 }}>AIニュース</span>
        </div>

        {/* Title */}
        <h1
          style={{
            fontSize: title.length > 40 ? '42px' : '52px',
            fontWeight: 700,
            color: 'white',
            textAlign: 'center',
            lineHeight: 1.3,
            marginBottom: '30px',
            letterSpacing: '-0.02em',
            textShadow: '0 2px 10px rgba(0, 0, 0, 0.3)',
          }}
        >
          {title}
        </h1>

        {/* Date */}
        <p
          style={{
            fontSize: '24px',
            color: 'rgba(255, 255, 255, 0.7)',
            fontWeight: 400,
          }}
        >
          {date}
        </p>
      </div>

      {/* Decorative elements */}
      <div
        style={{
          position: 'absolute',
          top: '60px',
          left: '60px',
          width: '80px',
          height: '80px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(100, 200, 255, 0.3) 0%, transparent 70%)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          bottom: '60px',
          right: '60px',
          width: '120px',
          height: '120px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(255, 100, 200, 0.3) 0%, transparent 70%)',
        }}
      />
    </div>
  );
}