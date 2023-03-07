#Author discoverrange
#!/bin/bash 
input="/iam/project.txt"
while IFS= read -r line
do

    proj="$line"
    for recom in $(gcloud recommender recommendations list --project=$proj --location=global --recommender=google.iam.policy.Recommender --format='value(RECOMMENDATION_ID)') ; do
        rec=$(gcloud recommender recommendations list --project=$proj --location=global --recommender=google.iam.policy.Recommender --format='value(RECOMMENDATION_ID)')
        echo $recom
        echo $(gcloud recommender recommendations describe $recom --project=$proj --recommender=google.iam.policy.Recommender --location=global --format=json) > $recom.json
        gsutil cp $recom.json gs://iamlogs/$proj/
        rm $recom.json
    done
    gsutil ls -r gs://iamlogs/$proj/** >file.txt
    echo "$line"
    python3 retrive.py $proj

done < "$input"