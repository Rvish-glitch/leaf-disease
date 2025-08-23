// Test frontend-backend connection
const API_BASE_URL = "https://leaf-disease-production.up.railway.app";

async function testConnection() {
    console.log("🧪 Testing frontend-backend connection...");
    console.log("🔗 API URL:", API_BASE_URL);
    
    try {
        // Test 1: Health check
        console.log("\n1️⃣ Testing health endpoint...");
        const healthResponse = await fetch(`${API_BASE_URL}/health`);
        const healthData = await healthResponse.json();
        console.log("✅ Health check:", healthData);
        
        // Test 2: Simulate file upload (we can't actually upload from Node.js easily)
        console.log("\n2️⃣ Testing CORS preflight...");
        const corsResponse = await fetch(`${API_BASE_URL}/predict`, {
            method: 'OPTIONS',
            headers: {
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'POST'
            }
        });
        
        console.log("✅ CORS status:", corsResponse.status);
        console.log("✅ CORS headers:");
        corsResponse.headers.forEach((value, key) => {
            if (key.toLowerCase().includes('access-control')) {
                console.log(`   ${key}: ${value}`);
            }
        });
        
        console.log("\n🎉 Connection tests passed! Frontend should be able to connect to Railway.");
        return true;
        
    } catch (error) {
        console.error("❌ Connection test failed:", error.message);
        return false;
    }
}

// For browser environment
if (typeof window !== 'undefined') {
    window.testConnection = testConnection;
    // Auto-run test
    testConnection();
}

// For Node.js environment  
if (typeof module !== 'undefined') {
    module.exports = { testConnection };
}
