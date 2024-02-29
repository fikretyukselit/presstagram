import React, { useEffect, useState } from "react";
import "./Presstagram.css";
import logo from "./yatay_logo.png";

const Presstagram = () => {
  const [images, setImages] = useState([]);
  const [lastPrintTime, setLastPrintTime] = useState(0);
  const [printDelay] = useState(15000);
  const [showCooldownWarning, setShowCooldownWarning] = useState(false);

  useEffect(() => {
    fetch("http://localhost:5000/images")
      .then((response) => response.json())
      .then((data) => setImages(data.images))
      .catch((error) => console.error("Failed to load images", error));
  }, []);

  const handleClick = (imageName) => {
    const currentTime = new Date().getTime();
    if (currentTime - lastPrintTime > printDelay) {
      setLastPrintTime(currentTime);
      setShowCooldownWarning(false);
      console.log(`Request sent for image: ${imageName}`);
      fetch(`http://localhost:5000/print/${imageName}`).catch((error) =>
        console.error("Failed to send request", error),
      );
    } else {
      setShowCooldownWarning(true);
    }
  };

  const handleCloseWarning = () => {
    setShowCooldownWarning(false);
  };

  useEffect(() => {
    const interval = setInterval(() => {
      fetch("http://localhost:5000/update_posts")
        .then((response) => response.json())
        .then((data) => console.log(data.message))
        .catch((error) => console.error("Failed request an update", error));
      fetch("http://localhost:5000/images")
        .then((response) => response.json())
        .then((data) => setImages(data.images))
        .then(() => console.log("Images updated"))
        .catch((error) => console.error("Failed to load images", error));
    }, 60000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <nav className="navbar">
        <div className="navbar-brand">
          <img
            src={logo}
            alt="Fikret Yuksel Foundation Logo"
            className="navbar-logo"
          />
          <div className="brand-text">Presstagram</div>
        </div>
      </nav>
      {showCooldownWarning && (
        <div className="cooldown-overlay">
          <div className="cooldown-warning">
            <div className="emoji-large">😉</div>
            <p>Please wait a bit before printing another image.</p>
            <button onClick={handleCloseWarning}>Close</button>
          </div>
        </div>
      )}
      <div className="gallery">
        {images.map((imageName, index) => (
          <div
            key={index}
            className="image-container"
            onClick={() => handleClick(imageName)}
          >
            <img
              src={`http://localhost:5000/images/${imageName}`}
              alt={imageName}
              className="image"
            />
          </div>
        ))}
      </div>
    </>
  );
};

export default Presstagram;
