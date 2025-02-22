import { useState } from "react";
import Buttons from "./components/Buttons";
import Input from "./components/Input";
import "../src/styles.css";

export default function Calculator() {
  const [equation, setEquation] = useState("0");
  const [totalEquation, setTotalEquation] = useState("");

  function handleButtonPress(value: string): void {
    if (value === "C") {
      setEquation("0");
      setTotalEquation("");
    } 
    else if (value === "=") {
      calculate();
    } 
    else if (value === "+/-") {
      setEquation((prev) => {
        // Toggle the negative sign
        if (prev === "0") return "-"; // Allow starting a negative number
        if (prev.startsWith("-")) {
          return prev.slice(1) || "0";
        } else {
          return "-" + prev;
        }
      });
    } 
    else if (["+", "-", "*", "/"].includes(value)) {
      if (equation !== "") {
        setTotalEquation((prev) => prev + equation + " " + value + " ");
        setEquation("0");
      }
    } 
    else {
      setEquation((prev) => (prev === "0" ? value : prev + value));
    }
  }

  async function calculate() {
    const fullEquation = totalEquation + equation;
    console.log(fullEquation)
  
    try {
      const response = await fetch("http://localhost:5000/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ equation: fullEquation }),
      });
  
      const data = await response.json();
      console.log(data)
      setEquation(data.result.toString());
      setTotalEquation(""); // Clear stored equation
    } catch (error) {
      console.error("Error:", error);
      setEquation("0");
    }
  }
  

  return (
    <div className="calculator-container">
      <Input error={false} input={totalEquation + equation} />
      <Buttons handleOnPress={handleButtonPress} />
    </div>
  );
}
