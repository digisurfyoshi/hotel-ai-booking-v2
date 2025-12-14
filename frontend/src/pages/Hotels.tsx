import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Hotel {
    id: number;
    name: string;
    address: string;
    owner_id: number;
}

const Hotels = () => {
    const [hotels, setHotels] = useState<Hotel[]>([]);
    const [name, setName] = useState('');
    const [address, setAddress] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        fetchHotels();
    }, []);

    const fetchHotels = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get('/api/hotels/', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setHotels(response.data);
        } catch (err) {
            console.error("Failed to fetch hotels", err);
        }
    };

    const handleCreateHotel = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        try {
            const token = localStorage.getItem('token');
            await axios.post('/api/hotels/', { name, address }, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setName('');
            setAddress('');
            fetchHotels();
        } catch (err) {
            console.error("Failed to create hotel", err);
            setError('Failed to create hotel');
        }
    };

    return (
        <div className="p-8">
            <h1 className="text-2xl font-bold mb-6">My Hotels</h1>

            <div className="bg-white p-6 rounded shadow mb-8">
                <h2 className="text-xl font-semibold mb-4">Add New Hotel</h2>
                {error && <p className="text-red-500 mb-2">{error}</p>}
                <form onSubmit={handleCreateHotel} className="flex gap-4 items-end">
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Hotel Name</label>
                        <input
                            type="text"
                            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Address</label>
                        <input
                            type="text"
                            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
                            value={address}
                            onChange={(e) => setAddress(e.target.value)}
                        />
                    </div>
                    <button
                        type="submit"
                        className="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700"
                    >
                        Add Hotel
                    </button>
                </form>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {hotels.map((hotel) => (
                    <div key={hotel.id} className="bg-white p-6 rounded shadow border border-gray-200">
                        <h3 className="text-lg font-bold text-gray-900">{hotel.name}</h3>
                        <p className="text-gray-600 mt-2">{hotel.address || 'No address provided'}</p>
                        <p className="text-xs text-gray-400 mt-4">ID: {hotel.id}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Hotels;
