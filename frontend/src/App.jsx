import { useState, useCallback } from 'react'
import Divider from '@mui/material/Divider';
import './App.css'
import FreeSolo from './assets/components/SearchBar'
import EnhancedTable from './assets/components/Table'
import AddButton from './assets/components/AddButton'
import ScrapeButton from './assets/components/ScrapeButton'
import Stack from '@mui/material/Stack';
import { height } from '@mui/system';


function App() {
  
  const [text, setText] = useState('');
  const [addFunction, setAddFunction] = useState(null);

  const handleAddFunction = useCallback((fn) => {
    setAddFunction(() => fn);
  }, []);

  return (
    <>
      <div style={{
        margin: 0,
        padding: 0,
        height: '95vh',
      }}>
        <Stack
          spacing={2}
          sx={{
            backgroundColor: 'white',
            margin: 0,
            padding: 0,
            height: '90vh',
            border: '1px solid grey',
            justifyContent: 'center', alignItems: 'center'

          }}
          divider={
            <Divider
              orientation='horizontal'
              flexItem
              variant='middle' />
          }>
          <div style={{ display: 'flex', margin: "8px", flexDirection: 'row', gap: '0.1', width: '25vw' }}>
            <div style={{ flexGrow: 10 }}>
              <FreeSolo setText={setText}/>
            </div>
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexGrow: 1}}>
              <AddButton text={text} onAdd={() => addFunction && addFunction(text)} />
            </div>
          </div>
            <ScrapeButton/>
          <EnhancedTable onAdd={handleAddFunction}/>
        </Stack>
      </div>
    </>
  )
}

export default App
