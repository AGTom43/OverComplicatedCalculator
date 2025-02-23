import { useState } from "react";
import Buttons from "./components/Buttons";
import Input from "./components/Input";
import "../src/styles.css";
import NeuralNet from "./nn_visuals/NeuralNet";
import { LayersConfig } from "./nn_visuals/NeuralNet";

// Example usage:
const exampleConfig: LayersConfig =[
    { units: 1 },
    {
      units: 8,
      fill: ["blue", "green", "red"],
      stroke: "black",
      strokeWidth: 0.5,
      radius: 5,
    },
    {
      units: 8,
      fill: ["red", "black", "red", "green", "yellow", "red", "black", "red"],
      stroke: "black",
      strokeWidth: 0.5,
      radius: 5,
    },
    { units: 1 },
  ]

export default function Calculator() {
  const [equation, setEquation] = useState("0");
  const [totalEquation, setTotalEquation] = useState("");
  const [LayersSetUp,setLayersSetUp] = useState([]);

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
      setEquation(data.nn_result.toString());
      setLayersSetUp(data.layers)
      setTotalEquation(""); // Clear stored equation
    } catch (error) {
      console.error("Error:", error);
      setEquation("0");
    }
  }
  
// TODO: restructure CSS for neural net
  return (
    <div className="calculator-container">
      <Input error={false} input={totalEquation + equation} />
      <Buttons handleOnPress={handleButtonPress} />
    <div className="neural-net-vis">
      <NeuralNet layersRepresentation={exampleConfig}/>
    </div>
    </div>
  );
}
