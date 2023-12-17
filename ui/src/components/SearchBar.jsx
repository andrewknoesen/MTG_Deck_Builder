import * as React from 'react';
import { useState, useEffect, useRef } from 'react';
import Paper from '@mui/material/Paper';
import InputBase from '@mui/material/InputBase';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';
import debounce from 'lodash/debounce';

import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';

export default function SearchBar({ placeholder, onSearch }) {

    const [options, setOptions] = useState([]);
    const [searchText, setSearchText] = useState('');

    const previousController = useRef();

    const getCards = (cardName) => {
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");

        var raw = JSON.stringify({
            "card": cardName
        });

        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
        };

        fetch("http://localhost:5000/flask/scryfall/fuzzy", requestOptions)
            .then(response => response.json())
            // .then(result => console.log("search term: " + cardName + ",results: " + result))
            .then(function (myJson) {
                console.log(
                    "search term: " + cardName + ", results (data field): ",
                    JSON.stringify(myJson.data)
                );
                const updatedOptions = myJson.data.map((p) => {
                    return { data: p };
                });
                setOptions(updatedOptions);
            })
            .catch(error => console.log('error', error));
    }

    const addCardsCollection = (name) => {
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        console.log("Got name: " + name)
        var raw = JSON.stringify({
            "name": name
        });

        var requestOptions = {
            method: 'PUT',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
        };

        fetch("http://localhost:5000/flask/postgres/upsert_collection_from_name", requestOptions)
            .then(response => response.json())
            .catch(error => console.log('error', error));
    }

    const onInputChange = (event, value, reason) => {
        if (value) {
            getCards(value);
            setSearchText(value);
        } else {
            setOptions([]);
        }
    };

    const handleButtonClick = () => {
        // Call the onSearch callback with the current searchText when the button is clicked
        console.log("Sending card for upsert: " + searchText)
        addCardsCollection(searchText);
        onSearch(searchText);
    };

    return (
        <Paper
            component="form"
            sx={{ p: '0.2rem 0.4rem', display: 'flex', alignItems: 'stretch', marginBottom: "1rem", flex: 1 }}
        >
            <IconButton sx={{ p: '1rem' }} aria-label="menu">
                <MenuIcon />
            </IconButton>
            <Divider sx={{ height: 'auto', m: 0.5 }} orientation="vertical" />
            <div style={{ flex: 1 }}>
                <Autocomplete
                    freeSolo
                    disableClearable
                    onInputChange={debounce(onInputChange, 300)}
                    options={options}
                    getOptionLabel={(option) => option.data}
                    renderInput={(params) => (
                        <TextField
                            {...params}
                            variant='outlined'
                            label={placeholder}
                            value={searchText}
                            InputProps={{
                                ...params.InputProps,
                                type: 'search',
                            }}
                            fullWidth={true}
                        />
                    )}
                />
            </div>
            <Divider sx={{ height: 'auto', m: 0.5 }} orientation="vertical" />
            <IconButton type="button" sx={{ p: '1rem' }} aria-label="search" onClick={handleButtonClick}>
                <SearchIcon />
            </IconButton>
        </Paper>

    );
}

