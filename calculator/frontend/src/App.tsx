import './App.css'
import '../src/styles.css'
import Calculator from './Calculator'
import EquationTree from './components/EquationTree'
import { useState } from 'react';

function App() {
  const [calculatedValues, setCalculatedValues] = useState([]);
  const [expression, setExpression] = useState('');

  return (
    <>
      <div>
        <h1>Overcomplicated Calculator</h1>
        <h2>An abacus for a less civilised age</h2>
        <Calculator setExpression={setExpression} setCalculatedValues={setCalculatedValues}/>
        <EquationTree expression={expression}/>
      </div>
    </>
  )
}

export default App
