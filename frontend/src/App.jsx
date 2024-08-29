import './App.css'
import OrderBuilder from './assets/screens/order_bulder/OrderBuilder'
import OrderSummary from './assets/screens/order_bulder/OrderSummary';

function App() {

  return (
    <>
      <div style={{ display: 'flex' }}>
        <OrderBuilder />
        <OrderSummary />
      </div>
    </>
  )
}

export default App
