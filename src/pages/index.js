import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

export default function Home() {
  return (
    <Layout
      title="Physical AI & Humanoid Robotics"
      description="Comprehensive guide to building intelligent humanoid robots"
    >
      <div style={{ padding: "2rem", textAlign: "center" }}>
        <h1>Physical AI & Humanoid Robotics</h1>
        <p>
          Comprehensive guide to building intelligent humanoid robots using ROS 2, simulation platforms, and AI technologies
        </p>
        
        <div style={{ display: "flex", gap: "1rem", justifyContent: "center", marginTop: "2rem" }}>
          <Link to="/docs/intro" className="button button--primary button--lg">
            Start Course
          </Link>
          <Link to="/docs/learning-paths/learning-paths" className="button button--secondary button--lg">
            Learning Paths
          </Link>
        </div>
      </div>

      {/* Custom Styles */}
      <style jsx>{`
        @keyframes glow {
          0%, 100% {
            opacity: 0.3;
          }
          50% {
            opacity: 0.6;
          }
        }

        @keyframes pulse-ring {
          0% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 0.3;
          }
          50% {
            transform: translate(-50%, -50%) scale(1.1);
            opacity: 0.1;
          }
          100% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 0.3;
          }
        }

        @media (max-width: 768px) {
          .ai-assistant-box {
            margin: 2rem 1rem !important;
            padding: 1.5rem !important;
          }
          
          .example-questions {
            grid-template-columns: 1fr !important;
            gap: 0.75rem !important;
          }
        }
      `}</style>
    </Layout>
  );
}
