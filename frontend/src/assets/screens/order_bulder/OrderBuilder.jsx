import * as React from 'react';
import { useState, useCallback } from 'react'
import Stack from '@mui/material/Stack'
import Divider from '@mui/material/Divider';

import FreeSolo from '../../components/SearchBar'
import EnhancedTable from '../../components/Table'
import AddButton from '../../components/AddButton'
import ScrapeButton from '../../components/ScrapeButton'
import QtyField from '../../components/QtyField';

function createData(name, qty) {
    return { name, qty };
}

export default function OrderBuilder({ setReport }) {
    const [text, setText] = useState('');
    const [qty, setQty] = useState(1);
    const [rows, setRows] = useState([])
    const updateRows = (name, qty) => {
        setRows((prevRows) => {
            const newRows = [...prevRows];
            const existingRow = newRows.find(row => row.name === name);
            if (existingRow) {
                if (qty === 0) {
                    // Remove the entry if qty is 0
                    return newRows.filter(row => row.name !== name);
                } else {
                    existingRow.qty = qty;  // Update if exists
                }
            } else {
                if (qty > 0) {
                    newRows.push(createData(name, qty));  // Create new entry if it doesn't exist
                }
            }
            return newRows;
        });
    };
    return (
        <div style={{
            margin: 0,
            padding: 0,
            height: '95vh',
        }}>
            <Stack
                spacing={2}
                sx={{
                    backgroundColor: 'white',
                    margin: 1,
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
                <div style={{ display: 'flex', margin: "8px", flexDirection: 'row', width: '30vw' }}>
                    <div style={{ flex: 8, padding: 10 }}>
                        <FreeSolo setText={setText} />
                    </div>
                    <div style={{ flex: 1, padding: 10 }}>
                        <QtyField setQty={setQty} />
                    </div>
                    <div style={{ flex: 1, padding: 10 }}>
                        <AddButton onAdd={() => updateRows(text, qty)} /> {/* using a call back so that the function is only called when the button is clicked */}
                    </div>
                </div>
                <ScrapeButton rows={rows} setReport={setReport} />
                <EnhancedTable rows={rows} handleQtyChange={updateRows} />
            </Stack>
        </div>
    );
}