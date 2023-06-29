import { useState } from 'react'

import Button from '@mui/material/Button';
import reactLogo from './../assets/react.svg'
import viteLogo from '/vite.svg'
import TopBar from './TopBar';
import SearchBar from './SearchBar';

import { ThemeProvider, createTheme } from '@mui/material/styles';

function AppBase({ title, children }) {
    const darkTheme = createTheme({
        palette: {
            mode: 'dark',
        },
    });

    return (

        <ThemeProvider theme={darkTheme}>
            <div>
                <TopBar title={title} />
            </div>
            <div style={{ alignContent: "right" }}>
                {children}
            </div>
        </ThemeProvider>
    )
}

export default AppBase
