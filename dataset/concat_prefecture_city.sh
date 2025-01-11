temp_dir="temp_unzip"                            
mkdir -p "$temp_dir"                 

# ZIPファイルを一括解凍し、CSVを収集して統合
for file in data/raw/*000-17.0b.zip; do          
    unzip -q "${file}" -d "$temp_dir" 
done

output_file="prefecture_city_lonlat.csv"    
: > "$output_file"  # 空ファイルを作成          
    
# すべてのCSVファイルを処理   
for csv_file in "$temp_dir"/*/*_2023.csv; do
    # 最初のファイルのヘッダーは残し、以降は削除
    if [ ! -s "$output_file" ]; then
        # ヘッダーを含めて出力                  
        cat "$csv_file" >> "$output_file"
    else
        # ヘッダーをスキップして追記
        tail -n +2 "$csv_file" >> "$output_file"
    fi
done

# 一時ディレクトリを削除
rm -rf "$temp_dir"

# 完了メッセージ
echo "All files processed and prefecture_city_lonlat.csv created."
