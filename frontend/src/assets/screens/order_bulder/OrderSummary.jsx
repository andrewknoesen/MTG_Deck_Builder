import * as React from 'react';
import Divider from '@mui/material/Divider';

import Stack from '@mui/material/Stack'

export default function OrderSummary() {
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
                <div style={{ display: 'flex', margin: "8px", flexDirection: 'row', width: '63vw' }}></div>
        </Stack>
        </div>
    )
}