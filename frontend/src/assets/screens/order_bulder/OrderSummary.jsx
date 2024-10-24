import * as React from 'react';
import Divider from '@mui/material/Divider';
import { useState, useCallback } from 'react'

import Stack from '@mui/material/Stack'
import { Typography } from '@mui/material';

import OrderBreakdown from '../../components/OrderBreakdown';
import OrderSummaryTitle from '../../components/OrderSummaryTitle';
import CostReport from '../../components/CostReport';
import ShippingBreakdown from '../../components/ShippingBreakdown';


function createData(name, qty) {
    return { name, qty };
}

export default function OrderSummary({ report }) {
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
                <OrderSummaryTitle />
                <div style={{ display: 'flex', margin: "8px", flexDirection: 'row' }}>
                    <OrderBreakdown report={report} />
                    <Divider orientation='vertical' flexItem variant='middle' />
                    <div style={{ flex: 1 }}>
                        <CostReport report={report} />
                        <Divider orientation='horizontal' flexItem variant='full' />
                        <ShippingBreakdown report={report} />
                    </div>
                </div>
            </Stack>
        </div>
    )
}