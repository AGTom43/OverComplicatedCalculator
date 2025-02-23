import './App.css'
import '../src/styles.css'
import Calculator from './Calculator'
import EquationTree from './components/EquationTree'

function App() {
  return (
    <>
      <div>
        <h1>Overcomplicated Calculator</h1>
        <h2>An abacus for a less civilised age</h2>
        <Calculator/>
        <EquationTree expression={'Expression(BinOp(BinOp(BinOp(Constant(1), Add(), Constant(2)), Mult(), BinOp(Constant(3), Sub(), Constant(4))), Mult(), BinOp(Constant(5), Sub(), Constant(6))))'}/>
      </div>
    </>
  )
}

export default App
