import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const testEndpoint = async (endpoint, method = 'get', data = null) => {
    try {
        let response;
        if (method === 'get') {
            response = await axios.get(`${API_URL}${endpoint}`);
        } else if (method === 'post') {
            response = await axios.post(`${API_URL}${endpoint}`, data);
        }
        console.log(`${endpoint} response:`, response);
        return response.data;
    } catch (error) {
        console.error(`Error from ${endpoint}:`, error.response || error);
        return null;
    }
};

export const startDebate = async () => {
    const debateData = {
        topic: "AI Ethics",
        name1: "Proponent",
        name2: "Opponent",
        questions: ["What are the main ethical concerns in AI development?"]
    };
    const response = await testEndpoint('/start_debate', 'post', debateData);
    return response && response.message.includes("Debate initialized");
};

export const oneTurnDebate = async () => {
    return await testEndpoint('/one_turn_debate', 'post');
};

export const getPersonas = async () => {
    return await testEndpoint('/persona', 'get');
};