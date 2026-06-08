const https = require('https');

// 从 worldcup26.ir 获取数据
function fetchData() {
    return new Promise((resolve, reject) => {
        const url = 'https://worldcup26.ir/get/games';
        
        https.get(url, (res) => {
            let data = '';
            
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    resolve(json);
                } catch (e) {
                    reject(e);
                }
            });
        }).on('error', (err) => {
            reject(err);
        });
    });
}

// 主函数
async function main() {
    try {
        console.log('正在从 worldcup26.ir 获取数据...');
        const data = await fetchData();
        
        console.log(`获取到 ${data.games?.length || 0} 场比赛数据`);
        
        // 保存到 matches.json
        const fs = require('fs');
        fs.writeFileSync('matches.json', JSON.stringify(data, null, 2));
        
        console.log('数据已保存到 matches.json');
    } catch (error) {
        console.error('获取数据失败:', error);
        process.exit(1);
    }
}

main();
