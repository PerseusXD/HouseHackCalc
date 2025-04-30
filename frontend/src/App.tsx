import React, { useEffect, useState } from "react";  
import axios from "axios";  
import { Container, Typography, Button, AppBar, Toolbar, Box } from "@mui/material";  

const App: React.FC = () => {  
    const [message, setMessage] = useState<string>("");  

    useEffect(() => {  
        axios.get("/api/")  
            .then(response => setMessage(response.data.message))  
            .catch(error => console.error("Error fetching data", error));  
    }, []);  

    return (  
        <>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        My App
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 2 }}>
                        <Button color="inherit">Home</Button>
                        <Button color="inherit">App</Button>
                    </Box>
                </Toolbar>
            </AppBar>
            <Container sx={{ mt: 4 }}>  
                <Typography variant="h3" gutterBottom>  
                    FastAPI + React + Vite + MUI (TypeScript)  
                </Typography>  
                <Typography variant="body1">  
                    {message || "Loading..."}  
                </Typography>  
                <Button variant="contained" color="primary" style={{ marginTop: '20px' }}>  
                    Material UI Button  
                </Button>  
            </Container>  
        </>
    );  
};  

export default App;