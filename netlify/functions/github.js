exports.handler = async function (event) {
    const path = event.queryStringParameters?.path;
    if (!path) return { statusCode: 400, body: 'path obrigatorio' };

    const url = `https://api.github.com${path}`;
    const res = await fetch(url, {
        headers: {
            'Accept': 'application/vnd.github+json',
            'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
        },
    });

    const body = await res.text();
    return {
        statusCode: res.status,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
        body,
    };
};
