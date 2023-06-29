import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import './index.css'
import DeckBuilder from './pages/DeckBuilder'
import Decks from './pages/Decks';
import Collection from './pages/Collection';

const router = createBrowserRouter([
  {
    path: "/",
    element: <App/>,
  },
  {
    path: "/deck_builder",
    element: <DeckBuilder/>,
  },
  {
    path: "/decks",
    element: <Decks/>,
  },
  {
    path: "/collection",
    element: <Collection/>,
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    {/* <App /> */}
    <RouterProvider router={router} />
  </React.StrictMode>,
)
