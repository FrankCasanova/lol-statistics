

// Declare variables
const playerSearchForm = document.querySelector('#playerSearchForm');
const playerName = document.querySelector('.player-name');
const playerInfo = document.querySelector('.player-info');
const championInfo = document.querySelector('.champion-info');
const performanceStats = document.querySelector('.performance-stats');
const rankAndMmr = document.querySelector('.rank-and-mmr');
const top5BestWr = document.querySelector('.top-5-best-wr-with-champ');
const championLore = document.querySelector('.champion-lore');

playerSearchForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const playerNameInput = document.querySelector('#playerName').value;
    const encodedPlayerName = encodeURIComponent(playerNameInput);
    const playerUrl = `http://127.0.0.1:8000/api/v1/playerprofile-data${encodedPlayerName}`;

    // Fetch the JSON file
    fetch(playerUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(jsonData => {
        console.log('JSON data:', jsonData);
        // Populate the HTML sections with JSON data
        playerName.innerHTML = 'Player Profile - ' + jsonData.champ_info.name;
        playerInfo.innerHTML = `
            <h2>Player Information</h2>
            <ul>
                <li><strong>Rank:</strong> ${jsonData.champ_info.rank}</li>
                <li><strong>LP:</strong> ${jsonData.champ_info.lp}</li>
                <li><strong>Main Role:</strong> ${jsonData.champ_info.main_role}</li>
            </ul>
            <div class="player-image">
                <img src="${jsonData.champ_info.profile_image}" alt="Player Profile Image">
            </div>
        `;

        championInfo.innerHTML = `
            <h2>Champion Information</h2>
            <div class="champion-image">
                <img src="${jsonData.champ_info.top_1_used_champ_image}" alt="Top 1 Used Champion Icon">
                <img src="${jsonData.champ_info.top_2_used_champ_image}" alt="Top 2 Used Champion Icon">
            </div>
            <ul>
                <li><strong>Top 1 Used Champion:</strong> ${jsonData.champ_info.top_1_used_champ}</li>
                <li><strong>Top 2 Used Champion:</strong> ${jsonData.champ_info.top_2_used_champ}</li>
            </ul>
        `;

        performanceStats.innerHTML = `
            <h2>Performance Stats</h2>
            <ul>
                <li><strong>Win Rate:</strong> ${jsonData.champ_info.win_rate}</li>
                <li><strong>Player Score:</strong> ${jsonData.champ_info.player_score}</li>
                <li><strong>Kill Participation:</strong> ${jsonData.champ_info.kill_participation}</li>
                <li><strong>Objective Participation:</strong> ${jsonData.champ_info.objetive_participation}</li>
                <li><strong>XP Diff vs Enemy:</strong> ${jsonData.champ_info.xp_diff_vs_enemy}</li>
            </ul>
        `;

        rankAndMmr.innerHTML = `
            <h2>Rank and MMR</h2>
            <ul>
                <li><strong>Rank Image:</strong> <img class="rank-image" src="${jsonData.champ_info.rank_image}" alt="Rank Image"></li>
                <li><strong>MMR:</strong> ${jsonData.mmr.mmr} ${jsonData.mmr.rank}</li>
            </ul>
        `;

        top5BestWr.innerHTML = `
            <h2>Top 5 Best Win Rates with Champion</h2>
            <table>
                <thead>
                    <tr>
                        <th>Player Name</th>
                        <th>Win Rate</th>
                        <th>Region</th>
                    </tr>
                </thead>
                <tbody>
                    ${jsonData.ingsingfull_info.top_5_best_wr_with_champ.map((player) => {
                        return `
                            <tr>
                                <td>${player.name}</td>
                                <td>${player.wr}</td>
                                <td>${player.region}</td>
                            </tr>
                        `;
                    }).join('')}
                </tbody>
            </table>
        `;

        championLore.innerHTML = `
            <h2>Champion Lore</h2>
            <p>${jsonData.wiki_info.lore}</p>
            <p>${jsonData.ingsingfull_info.brief_summary}</p>
            <p>${jsonData.ingsingfull_info.data_about_champ}</p>
        `;
    })
    .catch(error => {
        console.error('There was a problem fetching the JSON file:', error);
    });

});
    


