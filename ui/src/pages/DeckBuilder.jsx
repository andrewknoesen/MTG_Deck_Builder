import { useState } from 'react'

import AppBase from '../components/AppBase';
import SearchBar from '../components/SearchBar';
import { width } from '@mui/system';
import CardDisplayTable from '../components/CardDisplayTable';

function DeckBuilder() {

    return (
        <AppBase title="Deck Builder">
            <div style={{ alignSelf: "center", backgroundColor: "red", display: 'flex', flexGrow: 1, height: "80vh", width: "80vw"}}>
                <div style={{ backgroundColor:"blue", position:"fixed"}}>
                    <SearchBar placeholder="Search cards..."/>
                    <CardDisplayTable/>

                </div>
            </div>
        </AppBase>  
    )
}

export default DeckBuilder
