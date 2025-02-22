import './App.css'
import '../src/styles.css'
import Calculator from './Calculator'
import NeuralNet from './nn_visuals/NeuralNet'

function App() {
  return (
    <>
      <div>
        <h1>Overcomplicated Calculator</h1>
        <h2>An abacus for a less civilised age</h2>
        <Calculator/>
        <NeuralNet/>
      </div>
    </>
  )
}

export default App
