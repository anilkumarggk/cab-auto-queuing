<template>
    <div>
        <GlobalNavBar />
        <div class="uk-card uk-card-default uk-card-body uk-width-1-3@m uk-margin-top uk-margin-left" 
            v-if="!$route.params['user_id']">
            <h3 class="uk-card-title">Request a ride</h3>
            <form v-on:submit.prevent="request_ride">
                <div class="uk-margin">
                    <input class="uk-input" type="number" min="0"
                    placeholder="Enter the user ID" required v-model="user_id">
                </div>
                <button class="uk-button uk-button-primary">Request</button>
            </form>
        </div>
        <div class="uk-card uk-card-default uk-card-body uk-width-1-3@m uk-margin-top uk-margin-left" v-else>
            <router-link :to="{name: $route.name, params: {}}">
                <span uk-icon="arrow-left"></span> Request ride with a different USER ID
            </router-link>
            <div class="uk-text-center uk-margin-large-top uk-margin-large-bottom" v-if="fetching_rides">
                <div uk-spinner></div><br>
                <div class="uk-margin-small-right">Fetching your rides..</div>
            </div>
            <div class="uk-testing" v-else>
                <table class="uk-table uk-table-hover uk-table-small" v-if="user_rides.length >0" >
                    <caption class="uk-text-center">
                        <a @click="fetch_user_rides()">Refresh</a>
                    </caption>
                    <thead>
                    <th class="uk-text-left">Status</th>
                    <th class="uk-text-left">Driver</th>
                    <th class="uk-text-right">Ride requested on</th>
                    </thead>
                    <tbody>
                        <tr v-for="ride in user_rides" :key="ride.id">
                            <td class="uk-text-left">{{ ride.status }}</td>
                            <td class="uk-text-left">{{ ride.pickup_driver ? ride.pickup_driver : '-' }}</td>
                            <td class="uk-text-right">
                                {{ ride.modified_at | readable_format }}
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div v-else class="uk-margin-large-top uk-margin-large-bottom uk-text-center">
                    Your ride history will appear here..
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data () {
        return {
            user_id: undefined,
            fetching_rides: false,
            user_rides: []
        }
    },
    methods: {
        request_ride () {
            this.$http.post(
                '/api/user/ride/',
                { 'user_id': parseInt(this.user_id) }
            )
            .then(success => {
                this.$router.push({name: this.$route.name, params: {user_id: this.user_id}})
                this.fetch_user_rides()
            }, error => {
                alert(error)
            })
        },
        fetch_user_rides () {
            this.fetching_rides = true
            this.$http.get('/api/user/ride/?id=' + this.$route.params['user_id']).then(successResponse => {
                this.user_rides = successResponse.data.rides
                this.fetching_rides = false
            }, errorResponse => {
                debugger
                UIkit.notification({
                    message: 'Error fetching your rides :(',
                    status: 'danger',
                    pos: 'bottom-center',
                    timeout: 5000
                })
                this.fetching_rides = false
            })
        }
    },
    filters: {
        readable_format (timestamp) {
            let date_obj = new Date(timestamp)
            return date_obj.toDateString() + ' ' + date_obj.toLocaleTimeString()
        }
    },
    mounted () {
        if (typeof (this.$route.params['user_id']) !== 'undefined') {
            this.fetch_user_rides()
        }
    }
}
</script>
