import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

export default function Home() {
  return (
    <Layout
      title="Physical AI & Humanoid Robotics"
      description="Comprehensive 14-week course covering foundations, ROS 2, simulation, NVIDIA Isaac, humanoid development, and vision-language-action models"
    >
      <div style={{ 
        background: "#000000",
        minHeight: "100vh",
        position: "relative",
        overflow: "hidden",
        color: "#ffffff"
      }}>
        {/* Animated Background Elements */}
        <div style={{
          position: "absolute",
          top: "10%",
          left: "5%",
          width: "200px",
          height: "200px",
          background: "radial-gradient(circle, rgba(0, 255, 0, 0.1) 0%, transparent 70%)",
          borderRadius: "50%",
          filter: "blur(40px)",
          animation: "pulse 4s ease-in-out infinite"
        }} />
        <div style={{
          position: "absolute",
          top: "60%",
          right: "10%",
          width: "300px",
          height: "300px",
          background: "radial-gradient(circle, rgba(0, 255, 0, 0.05) 0%, transparent 70%)",
          borderRadius: "50%",
          filter: "blur(60px)",
          animation: "pulse 6s ease-in-out infinite reverse"
        }} />
        <div style={{
          position: "absolute",
          bottom: "20%",
          left: "15%",
          width: "150px",
          height: "150px",
          background: "radial-gradient(circle, rgba(0, 255, 0, 0.08) 0%, transparent 70%)",
          borderRadius: "50%",
          filter: "blur(30px)",
          animation: "pulse 3s ease-in-out infinite"
        }} />

        {/* Hero Section */}
        <div style={{ 
          position: "relative",
          zIndex: 2,
          padding: "4rem 2rem",
          textAlign: "center"
        }}>
          <div style={{
            display: "inline-block",
            padding: "0.5rem 1.5rem",
            background: "rgba(0, 255, 0, 0.1)",
            border: "1px solid rgba(0, 255, 0, 0.3)",
            borderRadius: "50px",
            marginBottom: "2rem"
          }}>
            <span style={{ fontSize: "0.9rem", fontWeight: "600", color: "#00ff00" }}>14-Week Comprehensive Course</span>
          </div>
          
          <h1 style={{ 
            fontSize: "3.5rem", 
            fontWeight: "800", 
            marginBottom: "1.5rem",
            color: "#ffffff",
            lineHeight: "1.2",
            textShadow: "0 0 20px rgba(0, 255, 0, 0.5)"
          }}>
            Physical AI &<br />Humanoid Robotics
          </h1>
          
          <p style={{ 
            fontSize: "1.3rem", 
            maxWidth: "700px", 
            margin: "0 auto 3rem",
            color: "#cccccc",
            lineHeight: "1.6"
          }}>
            Master the complete stack for building intelligent humanoid robots — from foundational concepts 
            to cutting-edge AI integration with vision-language-action models
          </p>
          
          <div style={{ display: "flex", gap: "1rem", justifyContent: "center", flexWrap: "wrap", marginBottom: "4rem" }}>
            <Link 
              to="/docs/intro"
              className="button button--primary button--lg"
              style={{
                background: "#00ff00",
                color: "#000000",
                border: "none",
                padding: "1rem 2rem",
                fontSize: "1.1rem",
                fontWeight: "600",
                borderRadius: "50px",
                boxShadow: "0 0 30px rgba(0, 255, 0, 0.5)",
                transition: "all 0.3s ease"
              }}
            >
              View Full Curriculum
            </Link>
          </div>
        </div>

        {/* Course Parts Grid */}
        <div style={{ 
          position: "relative",
          zIndex: 2,
          padding: "0 2rem 4rem",
          maxWidth: "1200px",
          margin: "0 auto"
        }}>
          <h2 style={{ 
            textAlign: "center", 
            color: "#ffffff", 
            fontSize: "2.5rem", 
            fontWeight: "700",
            marginBottom: "3rem",
            textShadow: "0 0 10px rgba(0, 255, 0, 0.3)"
          }}>
            Course Journey
          </h2>
          
          <div style={{ 
            display: "grid", 
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", 
            gap: "1.5rem"
          }}>
            {[
              { part: "I", title: "Foundations of Physical AI", weeks: "Weeks 1-2", desc: "Embodied Intelligence" },
              { part: "II", title: "ROS 2 - Robotic Nervous System", weeks: "Weeks 3-5", desc: "Core Concepts & Python" },
              { part: "III", title: "Digital Twin - Simulation", weeks: "Weeks 6-7", desc: "Gazebo & Unity" },
              { part: "IV", title: "AI-Robot Brain - NVIDIA Isaac", weeks: "Weeks 8-10", desc: "Perception & Navigation" },
              { part: "V", title: "Humanoid Robot Development", weeks: "Weeks 11-12", desc: "Kinematics & Locomotion" },
              { part: "VI", title: "Vision-Language-Action", weeks: "Week 13", desc: "LLMs & VLA Models" },
              { part: "VII", title: "Deployment & Integration", weeks: "Week 14", desc: "Capstone Project" }
            ].map((item, index) => (
              <div
                key={index}
                style={{
                  background: "rgba(0, 255, 0, 0.05)",
                  border: "1px solid rgba(0, 255, 0, 0.2)",
                  borderRadius: "20px",
                  padding: "2rem",
                  textAlign: "center",
                  transition: "all 0.3s ease",
                  cursor: "pointer",
                  transform: "translateY(0)"
                }}
                onMouseEnter={(e) => {
                  e.target.style.transform = "translateY(-10px) scale(1.05)";
                  e.target.style.boxShadow = "0 0 40px rgba(0, 255, 0, 0.3)";
                  e.target.style.background = "rgba(0, 255, 0, 0.1)";
                  e.target.style.borderColor = "rgba(0, 255, 0, 0.4)";
                }}
                onMouseLeave={(e) => {
                  e.target.style.transform = "translateY(0) scale(1)";
                  e.target.style.boxShadow = "none";
                  e.target.style.background = "rgba(0, 255, 0, 0.05)";
                  e.target.style.borderColor = "rgba(0, 255, 0, 0.2)";
                }}
              >
                <div style={{
                  display: "inline-block",
                  background: "rgba(0, 255, 0, 0.15)",
                  padding: "0.3rem 0.8rem",
                  borderRadius: "20px",
                  fontSize: "0.8rem",
                  fontWeight: "600",
                  marginBottom: "1rem",
                  color: "#00ff00"
                }}>
                  Part {item.part}
                </div>
                <h3 style={{ color: "#ffffff", fontSize: "1.2rem", fontWeight: "700", marginBottom: "0.5rem" }}>
                  {item.title}
                </h3>
                <p style={{ color: "#00ff00", fontSize: "0.9rem", fontWeight: "600", margin: "0.5rem 0" }}>
                  {item.weeks}
                </p>
                <p style={{ color: "#aaaaaa", fontSize: "0.85rem", margin: 0 }}>
                  {item.desc}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Stats Section */}
        <div style={{ 
          position: "relative",
          zIndex: 2,
          padding: "2rem",
          textAlign: "center",
          background: "rgba(0, 255, 0, 0.05)",
          borderTop: "1px solid rgba(0, 255, 0, 0.2)",
          borderBottom: "1px solid rgba(0, 255, 0, 0.2)"
        }}>
          <div style={{ 
            display: "grid", 
            gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", 
            gap: "2rem",
            maxWidth: "800px",
            margin: "0 auto"
          }}>
            <div>
              <div style={{ fontSize: "2.5rem", fontWeight: "800", color: "#00ff00", marginBottom: "0.5rem" }}>30</div>
              <div style={{ color: "#cccccc", fontSize: "0.9rem" }}>Comprehensive Chapters</div>
            </div>
            <div>
              <div style={{ fontSize: "2.5rem", fontWeight: "800", color: "#00ff00", marginBottom: "0.5rem" }}>14</div>
              <div style={{ color: "#cccccc", fontSize: "0.9rem" }}>Weeks of Learning</div>
            </div>
            <div>
              <div style={{ fontSize: "2.5rem", fontWeight: "800", color: "#00ff00", marginBottom: "0.5rem" }}>7</div>
              <div style={{ color: "#cccccc", fontSize: "0.9rem" }}>Major Parts</div>
            </div>
            <div>
              <div style={{ fontSize: "2.5rem", fontWeight: "800", color: "#00ff00", marginBottom: "0.5rem" }}>∞</div>
              <div style={{ color: "#cccccc", fontSize: "0.9rem" }}>Possibilities</div>
            </div>
          </div>
        </div>

        {/* Technology Stack */}
        <div style={{ 
          position: "relative",
          zIndex: 2,
          padding: "3rem 2rem",
          textAlign: "center"
        }}>
          <h2 style={{ 
            color: "#ffffff", 
            fontSize: "2rem", 
            fontWeight: "700",
            marginBottom: "2rem",
            textShadow: "0 0 10px rgba(0, 255, 0, 0.3)"
          }}>
            Technology Stack
          </h2>
          <div style={{ 
            display: "flex", 
            gap: "1rem", 
            justifyContent: "center", 
            flexWrap: "wrap",
            maxWidth: "800px",
            margin: "0 auto"
          }}>
            {[
              "ROS 2", "Gazebo", "NVIDIA Isaac", "Humanoid Robots", 
              "Vision-Language-Action", "Python", "Unity", "Edge Computing"
            ].map((tech, index) => (
              <span
                key={index}
                style={{
                  background: "rgba(0, 255, 0, 0.1)",
                  border: "1px solid rgba(0, 255, 0, 0.3)",
                  padding: "0.8rem 1.5rem",
                  borderRadius: "25px",
                  fontSize: "0.95rem",
                  fontWeight: "600",
                  color: "#00ff00",
                  transition: "all 0.3s ease"
                }}
                onMouseEnter={(e) => {
                  e.target.style.background = "rgba(0, 255, 0, 0.2)";
                  e.target.style.transform = "translateY(-2px)";
                  e.target.style.boxShadow = "0 0 20px rgba(0, 255, 0, 0.4)";
                }}
                onMouseLeave={(e) => {
                  e.target.style.background = "rgba(0, 255, 0, 0.1)";
                  e.target.style.transform = "translateY(0)";
                  e.target.style.boxShadow = "none";
                }}
              >
                {tech}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* CSS Animations */}
      <style jsx={true}>{`
        @keyframes pulse {
          0%, 100% {
            opacity: 0.3;
            transform: scale(1);
          }
          50% {
            opacity: 0.8;
            transform: scale(1.1);
          }
        }

        @media (max-width: 768px) {
          h1 {
            font-size: 2.5rem !important;
          }
          
          .course-grid {
            grid-template-columns: 1fr !important;
            gap: 1rem !important;
          }
        }
      `}</style>
    </Layout>
  );
}
