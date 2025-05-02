import React, { useEffect, useState } from "react";
import axios from "axios";
import { Typography, Box, CircularProgress, Pagination, IconButton } from "@mui/material";
import { useNavigate } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ListingBlock from "./ListingBlock";

interface Listing {
    formattedAddress: string;
    city: string;
    state: string;
    zipCode: string;
    price: number;
    bedrooms?: number;
    bathrooms?: number;
    squareFootage?: number;
}

interface ApiResponse {
    [zipCode: string]: Listing[];
}

const ITEMS_PER_PAGE = 10;

const ListingsPage: React.FC = () => {
    const [listings, setListings] = useState<Listing[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [page, setPage] = useState(1);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchListings = async () => {
            try {
                const response = await axios.get<ApiResponse>("http://localhost:8000/state/VA");
                const allListings = Object.values(response.data).flat();
                setListings(allListings);
                setError(null);
            } catch (err) {
                setError("Failed to fetch listings. Please try again later.");
                console.error("Error fetching listings:", err);
            } finally {
                setLoading(false);
            }
        };

        fetchListings();
    }, []);

    const handlePageChange = (event: React.ChangeEvent<unknown>, value: number) => {
        setPage(value);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const paginatedListings = listings.slice(
        (page - 1) * ITEMS_PER_PAGE,
        page * ITEMS_PER_PAGE
    );

    const totalPages = Math.ceil(listings.length / ITEMS_PER_PAGE);

    return (
        <Box sx={{ 
            minHeight: '100vh',
            width: '100vw',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            bgcolor: 'background.default'
        }}>
            <Box sx={{ 
                width: '100%',
                maxWidth: '1200px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                px: 2,
                py: 4
            }}>
                <Box sx={{ 
                    width: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    mb: 4
                }}>
                    <IconButton 
                        onClick={() => navigate('/')}
                        sx={{ mr: 2 }}
                    >
                        <ArrowBackIcon />
                    </IconButton>
                    <Typography 
                        variant="h4" 
                        component="h1" 
                        align="center"
                        sx={{ flex: 1 }}
                    >
                        Virginia Property Listings
                    </Typography>
                </Box>
                
                {loading ? (
                    <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
                        <CircularProgress />
                    </Box>
                ) : error ? (
                    <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
                        <Typography color="error" align="center">
                            {error}
                        </Typography>
                    </Box>
                ) : (
                    <>
                        <Box sx={{ 
                            width: '100%',
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            gap: 1.5
                        }}>
                            {paginatedListings.map((listing, index) => (
                                <Box 
                                    key={`${listing.formattedAddress}-${index}`} 
                                    sx={{ 
                                        width: '100%', 
                                        display: 'flex', 
                                        justifyContent: 'center'
                                    }}
                                >
                                    <ListingBlock {...listing} />
                                </Box>
                            ))}
                        </Box>
                        <Box 
                            display="flex" 
                            justifyContent="center" 
                            mt={4}
                            mb={2}
                        >
                            <Pagination 
                                count={totalPages}
                                page={page}
                                onChange={handlePageChange}
                                color="primary"
                                size="large"
                            />
                        </Box>
                    </>
                )}
            </Box>
        </Box>
    );
};

export default ListingsPage; 