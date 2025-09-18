# main.py
import pandas as pd
from data_extractor import extract_text_from_url
from text_analyzer import analyze_text
import os
import time

def main():
    print("🚀 Starting Blackcoffer Text Analysis Assignment...")
    
    # Load input URLs
    input_df = pd.read_excel('input/Input.xlsx')
    print(f"📄 Loaded {len(input_df)} URLs from Input.xlsx")
    
    results = []
    consecutive_failures = 0
    max_consecutive_failures = 2  # Pause after 2 failures

    # Process each URL
    for index, row in input_df.iterrows():
        url_id = row['URL_ID']
        url = row['URL']
        
        print(f"\n🔍 Processing {index + 1}/{len(input_df)}: {url_id}")
        
        # Extract text
        article_text = extract_text_from_url(url)
        if not article_text.strip():
            print(f"⚠️  No text extracted for {url_id}")
            consecutive_failures += 1
            
            if consecutive_failures >= max_consecutive_failures:
                print(f"🚫 Too many consecutive failures ({max_consecutive_failures}). Pausing for 45 seconds...")
                time.sleep(45)
                consecutive_failures = 0
                
            # Append empty result
            empty_result = {col: "" for col in [
                "POSITIVE SCORE", "NEGATIVE SCORE", "POLARITY SCORE", "SUBJECTIVITY SCORE",
                "AVG SENTENCE LENGTH", "PERCENTAGE OF COMPLEX WORDS", "FOG INDEX",
                "AVG NUMBER OF WORDS PER SENTENCE", "COMPLEX WORD COUNT", "WORD COUNT",
                "SYLLABLE PER WORD", "PERSONAL PRONOUNS", "AVG WORD LENGTH"
            ]}
            empty_result['URL_ID'] = url_id
            empty_result['URL'] = url
            results.append(empty_result)
            continue
        
        consecutive_failures = 0  # Reset on success
        
        print(f"✅ Extracted {len(article_text)} characters")
        
        # Analyze text
        try:
            analysis = analyze_text(article_text)
            analysis['URL_ID'] = url_id
            analysis['URL'] = url
            results.append(analysis)
            print(f"📈 Analysis completed for {url_id}")
        except Exception as e:
            print(f"❌ Error analyzing {url_id}: {str(e)}")
            continue
    
    # Create output DataFrame
    output_df = pd.DataFrame(results)
    
    # Reorder columns to match Output Data Structure.xlsx
    column_order = [
        "URL_ID", "URL", "POSITIVE SCORE", "NEGATIVE SCORE", "POLARITY SCORE",
        "SUBJECTIVITY SCORE", "AVG SENTENCE LENGTH", "PERCENTAGE OF COMPLEX WORDS",
        "FOG INDEX", "AVG NUMBER OF WORDS PER SENTENCE", "COMPLEX WORD COUNT",
        "WORD COUNT", "SYLLABLE PER WORD", "PERSONAL PRONOUNS", "AVG WORD LENGTH"
    ]
    
    output_df = output_df.reindex(columns=column_order)
    
    # Save to Excel
    output_path = 'output/Output_Data_Structure.xlsx'
    output_df.to_excel(output_path, index=False)
    print(f"\n🎉 Results saved to {output_path}")
    print(f"📊 Processed {len(results)} articles successfully!")

if __name__ == "__main__":
    main()