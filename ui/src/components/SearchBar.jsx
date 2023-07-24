import * as React from 'react';
import Paper from '@mui/material/Paper';
import InputBase from '@mui/material/InputBase';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';

export default function SearchBar({placeholder}) {



    return (
        <Paper
            component="form"
            sx={{ p: '0.2rem 0.4rem', display: 'flex', alignItems: 'stretch', marginBottom: "1rem", flex: 1}}
        >
            <IconButton sx={{ p: '1rem' }} aria-label="menu">
                <MenuIcon />
            </IconButton>
            <InputBase
                sx={{ ml: 1, flex: 1 }}
                placeholder={placeholder}
                inputProps={{ 'aria-label': 'search google maps' }}
            />

            <Divider sx={{ height: 28, m: 0.5 }} orientation="vertical" />
            <IconButton type="button" sx={{ p: '1rem' }} aria-label="search">
                <SearchIcon />
            </IconButton>
        </Paper>
    );
}