function draw_degree_in_graph()
    dataset = csvread('./data/graph/degree_in_graph.csv', 1, 1);
    disp(mean(dataset(:,1)));
    disp(mean(dataset(:,2)));
    disp(mean(dataset(:,3)));
    disp(mean(dataset(:,4)));
    figure(1);
    h1 = cdfplot(dataset(:,1));
    set(h1, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    xlim([0, 200]);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel('In-degree','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    title('');
    grid off;
    print('./results/graph/CDF_indegree.eps', '-depsc');
    
    figure(2);
    h2 = cdfplot(dataset(:,2));
    set(h2, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    xlim([0, 200]);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel('Out-degree','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    title('');
    grid off;
    print('./results/graph/CDF_outdegree.eps', '-depsc');
    
    figure(3);
    h3 = cdfplot(dataset(:,3));
    set(h3, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    set(gca,'XScale','log');
    xlim([0.1 10]);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel('Balance','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    title('');
    grid off;
    print('./results/graph/CDF_balance.eps', '-depsc');
    
    
    num_0 = nnz(dataset(:,3) < 0.5);
    num_1 = nnz(dataset(:,3) >= 0.5 & dataset(:,3) <= 2);
    num_2 = nnz(dataset(:,3) > 2);
    num_3 = nnz(dataset(:,3) < 1);
    tot = length(dataset(:,3));
    
    disp(num_0/tot);
    disp(num_1/tot);
    disp(num_2/tot);
    disp(num_3/tot);
    
    figure(4);
    h4 = cdfplot(dataset(:,4));
    set(h4, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel('Reciprocity','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    title('');
    grid off;
    print('./results/graph/CDF_reciprocity.eps', '-depsc');
    
    num_0 = nnz(dataset(:,4) == 0);
    tot = length(dataset(:,4));
    disp(num_0/tot);
    
    figure(5);
    [ycdf,xcdf] = cdfcalc(dataset(:,1));
    xccdf = xcdf;
    yccdf = 1-ycdf(1:end-1);
    loglog(xccdf, yccdf, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    xlim([0, 10000000]);
    set(gca, 'FontSize', 12);
    xlabel('In-degree','FontSize',20);
    ylabel('CCDF','FontSize',20);
    title('');
    grid off;
    print('./results/graph/CCDF_indegree.eps', '-depsc');
    
    figure(6);
    [ycdf,xcdf] = cdfcalc(dataset(:,2));
    xccdf = xcdf;
    yccdf = 1-ycdf(1:end-1);
    loglog(xccdf, yccdf, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    xlim([0, 100000]);
    set(gca, 'FontSize', 12);
    xlabel('Out-degree','FontSize',20);
    ylabel('CCDF','FontSize',20);
    title('');
    grid off;
    print('./results/graph/CCDF_outdegree.eps', '-depsc');
    
    figure(7);
    [ycdf,xcdf] = cdfcalc(dataset(:,2));
    xccdf = xcdf;
    yccdf = 1-ycdf(1:end-1);
    loglog(xccdf, yccdf, 'color', 'b', 'LineStyle', '-', 'LineWidth', 2);
    hold on;
    [ycdf,xcdf] = cdfcalc(dataset(:,1));
    xccdf = xcdf;
    yccdf = 1-ycdf(1:end-1);
    loglog(xccdf, yccdf, 'color', 'r', 'LineStyle', '--', 'LineWidth', 2);
    xlim([0, 10000000]);
    set(gca, 'FontSize', 12);
    xlabel('Out-degree/In-degree','FontSize',20);
    ylabel('CCDF','FontSize',20);
    legend('Out-degree', 'In-degree');
    set(legend, 'FontSize', 20);
    title('');
    grid off;
    print('./results/graph/CCDF_outdegree_indegree.eps', '-depsc');
end