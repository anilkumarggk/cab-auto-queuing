<template lang="html">
    <div>
        <GlobalNavBar />
        <div uk-grid class="uk-flex-center">
            <div class="uk-width-1-2@m uk-padding uk-margin-large-top uk-text-center"
                v-if="fetching_rides">
                <div uk-spinner></div>
                <p>Fetching ride data.. </p>
            </div>
            <div class="uk-width-1-2@m" v-else>
                <ul class="uk-pagination uk-flex-right uk-margin-medium-top" uk-margin v-if="page_links.length > 1">
                    
                    <li v-for="page in page_links" :class="{'uk-active': page[2], 'uk-disabled': page[3]}">
                        <router-link :to="{ name: $route.name, query: {page: page[1]} }">
                            {{ page[3]?'...':page[1] }}
                        </router-link>
                    </li>
                    
                    
                    <!-- <li><a href="#"><span uk-pagination-previous></span></a></li> -->                    
                    <!-- <li><a href="#"><span uk-pagination-next></span></a></li> -->
                </ul>
                <table class="uk-table uk-table-striped" v-if="rides.length>0">
                    <thead>
                        <tr>
                            <th>Ride ID</th>
                            <th>Status</th>
                            <th>Requested at</th>
                            <th>Driver</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="ride in rides" :key="ride.id">
                            <td># {{ ride.id }}</td>
                            <td>{{ ride.status }}</td>
                            <td>{{ ride.created_at }}</td>
                            <td>{{ ride.pickup_driver || '-' }}</td>
                        </tr>
                    </tbody>
                </table>
                <div class="uk-width-1-2@m uk-padding uk-margin-large-top uk-text-center"
                    v-else>
                    <p>No ride data available.</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            rides: [],
            page_links: [],
            // results_per_page: 10,
            // total_results: 0,
            fetching_rides: false
        }
    },
    methods: {
        fetch_rides () {
            this.fetching_rides = true;
            let current_page = this.$route.query['page'] || 1;
            this.$http.get('/api/dashboard/?page=' + current_page).then(
                successResponse => {
                    debugger;
                    this.rides = successResponse.body.results;
                    this.page_links = successResponse.body.page_links;
                    this.fetching_rides = false;
                }, 
                errorResponse => {
                    this.fetching_rides = false;                    
                }
            )
        }
    },
    created() {
        this.fetch_rides()
    },
    watch: {
        '$route.query': function(new_val, old_val){
            this.fetch_rides()
        }
    }
}
</script>

<style lang="css" scoped>
    .uk-active {
        font-weight: bold;
        text-decoration: underline;
    }
</style>
