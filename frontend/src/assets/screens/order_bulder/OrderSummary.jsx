import * as React from 'react';
import Divider from '@mui/material/Divider';
import { useState, useCallback } from 'react'

import Stack from '@mui/material/Stack'
import { Typography } from '@mui/material';

import EnhancedTable from '../../components/Table'


function createData(name, qty) {
    return { name, qty };
}

export default function OrderSummary() {
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
    }
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
                    width: '64vw',
                    height: '90vh',
                    border: '1px solid grey',
                }}
                divider={
                    <Divider
                        orientation='horizontal'
                        flexItem
                        variant='middle' />
                }>
                <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                    <Typography variant="h3" sx={{ color: 'black', padding: 1 }}>
                        Order Summary
                    </Typography>
                </div>
                <div style={{ display: 'flex', margin: "8px", flexDirection: 'row', height: '100%' }}>
                    <div style={{ flex: 1}}>
                        <div style={{ alignItems: 'start' }}>
                            <div style={{ display: 'flex', alignItems: 'start' }}>
                                <Typography variant="h6" sx={{ color: 'black', padding: 1 }}>
                                    Items
                                </Typography>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'start' }}>
                                <EnhancedTable rows={rows} handleQtyChange={updateRows} />

                            </div>
                        </div>
                    </div>

                    <Divider orientation='vertical' flexItem variant='middle' />

                    <div style={{ flex: 1 }}>
                        <div style={{ alignItems: 'start' }}>
                            <div style={{ display: 'flex', alignItems: 'start' }}>
                                <Typography variant="h6" sx={{ color: 'black', padding: 1 }}>
                                    Shipping Breakdown
                                </Typography>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'start' }}>
                                <Typography variant="body1" sx={{ color: 'black', padding: 1 }}>
                                    Test
                                </Typography>
                            </div>
                        </div>

                        <Divider orientation='horizontal' flexItem variant='full' />

                        <div style={{ alignItems: 'start' }}>
                            <div style={{ display: 'flex', alignItems: 'start' }}>
                                <Typography variant="h6" sx={{ color: 'black', padding: 1 }}>
                                    Total Cost
                                </Typography>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'start' }}>
                                <Typography variant="body1" sx={{ color: 'black', padding: 1 }}>
                                    Test
                                </Typography>
                            </div>
                        </div>
                    </div>
                </div>
            </Stack>
        </div>
    )
}