function draw_csl_simi()
    fid = fopen('./data/cross-site-linking/username_simi.csv', 'rt');
    C = textscan(fid, '%f %s', 'Delimiter', ',', 'HeaderLines', 1);
    fclose(fid);
    simi = C{1};
    figure(1);
    h = cdfplot(simi);
    set(h, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel('Similarity','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    title('');
    grid off;
    print('./results/csl/CDF_similarity_username.eps', '-depsc');
    
    fid = fopen('./data/cross-site-linking/name_simi.csv', 'rt');
    C = textscan(fid, '%f %s', 'Delimiter', ',', 'HeaderLines', 1);
    fclose(fid);
    simi = C{1};
    figure(2);
    h = cdfplot(simi);
    set(h, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel('Similarity','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    title('');
    grid off;
    print('./results/csl/CDF_similarity_name.eps', '-depsc');
    
    fid = fopen('./data/cross-site-linking/bio_simi.csv', 'rt');
    C = textscan(fid, '%f %s', 'Delimiter', ',', 'HeaderLines', 1);
    fclose(fid);
    simi = C{1};
    figure(3);
    h = cdfplot(simi);
    set(h, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel('Similarity','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    title('');
    grid off;
    print('./results/csl/CDF_similarity_bio.eps', '-depsc');
end