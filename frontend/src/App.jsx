import './App.css'
import OrderBuilder from './assets/screens/order_bulder/OrderBuilder'
import OrderSummary from './assets/screens/order_bulder/OrderSummary';
import { useState, useEffect, useCallback } from 'react'

function App() {

  const [report, setReport] = useState([]);
    

  return (
    <>
      <div style={{ display: 'flex' }}>
        <OrderBuilder setReport={setReport} />
        <OrderSummary report={report} />
      </div>
    </>
  )
}

export default App
