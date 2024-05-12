// Declare variables
const playerSearchForm = document.querySelector('#playerSearchForm');
const playerName = document.querySelector('.player-name');
const playerInfo = document.querySelector('.player-info');
const championInfo = document.querySelector('.champion-info');
const performanceStats = document.querySelector('.performance-stats');
const rankAndMmr = document.querySelector('.rank-and-mmr');
const top5BestWr = document.querySelector('.top-5-best-wr-with-champ');
const championLore = document.querySelector('.champion-lore');



// Define a function to handle the form submission
async function handleFormSubmission(event) {
    event.preventDefault();
    
    const playerNameInput = document.querySelector('#playerName').value;
    const encodedPlayerName = encodeURIComponent(playerNameInput);
    const playerUrl = `http://127.0.0.1:8000/api/v1/playerprofile-data${encodedPlayerName}`;

    // Fetch the JSON file
    const response = await fetch(playerUrl);
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    const jsonData = await response.json();

            // Populate the HTML sections with JSON data
            playerName.textContent = `Player Profile - ${jsonData.champ_info.name}`;

            const playerInfoHTML = `
                <h2>Player Information</h2>
                <div class="player-image">
                    <img src="${jsonData.champ_info.profile_image}" alt="Player Profile Image">
                </div>
                <ul>
                    <li><strong>Rank:</strong> ${jsonData.champ_info.rank}</li>
                    <li><strong>MMR:</strong> ${jsonData.mmr.mmr} ${jsonData.mmr.rank}</li>
                    <li><strong>LP:</strong> ${jsonData.champ_info.lp}</li>
                    <li><strong>Main Role:</strong> ${jsonData.champ_info.main_role}</li>
                    <li><strong>Ladder Rank:</strong> ${jsonData.ladder_rank.ladder_rank}</li>
                </ul>
                
            `;
            playerInfo.innerHTML = playerInfoHTML;

            const championInfoHTML = `
                <h2>Champion Information</h2>
                <div class="champion-image">
                    <img src="${jsonData.champ_info.top_1_used_champ_image}" alt="Top 1 Used Champion Icon">
                    <img src="${jsonData.champ_info.top_2_used_champ_image}" alt="Top 2 Used Champion Icon">
                </div>
                <ul>
                    <li><strong>Top 1 Used Champion:</strong> ${jsonData.champ_info.top_1_used_champ}</li>
                    <li><strong>Top 2 Used Champion:</strong> ${jsonData.champ_info.top_2_used_champ}</li>
                </ul>
                <ul>
                <h4>Top 3 Mastery</h4>
                ${jsonData.mastery.top_3_mastery.map(mastery => `<li><strong>${mastery.name}:</strong> ${mastery.amount} points</li>`).join('')}
            </ul>
            `;
            championInfo.innerHTML = championInfoHTML;

            const performanceStatsHTML = `
                <h2>Performance Stats</h2>
                <ul>
                    <li><strong>Win Rate:</strong> ${jsonData.champ_info.win_rate}</li>
                    <li><strong>Player Score:</strong> ${jsonData.champ_info.player_score}</li>
                    <li><strong>Kill Participation:</strong> ${jsonData.champ_info.kill_participation}</li>
                    <li><strong>Objective Participation:</strong> ${jsonData.champ_info.objetive_participation}</li>
                    <li><strong>XP Diff vs Enemy:</strong> ${jsonData.champ_info.xp_diff_vs_enemy}</li>
                </ul>
            `;
            performanceStats.innerHTML = performanceStatsHTML;

            // const rankAndMmrHTML = `
            //     <h2>Rank and MMR</h2>
            //     <ul>
            //         <img class="rank-image" src="${jsonData.champ_info.rank_image}" alt="Rank Image"></li>
            //         <li><strong>MMR:</strong> ${jsonData.mmr.mmr} ${jsonData.mmr.rank}</li>
            //     </ul>
            // `;
            // rankAndMmr.innerHTML = rankAndMmrHTML;

            const top5BestWrHTML = `
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
            top5BestWr.innerHTML = top5BestWrHTML;

            const championLoreHTML = `
                <h2>Champion Lore</h2>
                <p>${jsonData.wiki_info.lore}</p>
                <p>${jsonData.ingsingfull_info.brief_summary}</p>
                <p>${jsonData.ingsingfull_info.data_about_champ}</p>
            `;
            championLore.innerHTML = championLoreHTML;
        }

// Add the event listener to the form
playerSearchForm.addEventListener('submit', handleFormSubmission);


