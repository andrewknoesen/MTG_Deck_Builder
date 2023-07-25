import { useState } from 'react'

import AppBase from '../components/AppBase';
import SearchBar from '../components/SearchBar';

import Box from '@mui/material/Box';
import { width } from '@mui/system';
import CardDisplayTable from '../components/CardDisplayTable';

function DeckBuilder() {

    const baseStyle = {
        display: 'flex',
        alignItems: 'flex-start',
        justifyContent: 'flex_start',
        marginTop: '4.5rem',
        backgroundColor: 'red',
    };

    const collectionSearchStyle = {
        display: 'flex',
        alignItems: 'stretch',
        justifyContent: 'flex_start',
        backgroundColor: 'green',
        width: '20vw'

    };

    const buildPlateStyle = {
        display: 'flex',
        alignItems: 'stretch',
        justifyContent: 'flex_start',
        backgroundColor: 'yellow',
        width: '80vw',


    };

    return (
        <AppBase title="Deck Builder">
            <div
                style={baseStyle}
            >
                <div style={buildPlateStyle}>
                    <div style={{ flex: 1 }}>
                        <SearchBar placeholder="Search cards..." />

                        <CardDisplayTable />
                    </div>


                </div>
            </div>

        </AppBase>
    )
}

export default DeckBuilder
